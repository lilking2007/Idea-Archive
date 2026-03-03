package com.audiolog.app.service

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.media.MediaRecorder
import android.os.Build
import android.os.Environment
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.audiolog.app.MainActivity
import com.audiolog.app.R
import com.audiolog.app.data.RecorderRepository.updateDuration
import com.audiolog.app.data.RecorderRepository.setRecordingState
import com.audiolog.app.data.StorageManager
import com.audiolog.app.data.PreferencesManager
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.first
import java.io.File
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.TimeUnit

class AudioRecorderService : Service() {

    private val CHANNEL_ID = "recording_channel"
    private val SERVICE_ID = 1

    private var mediaRecorder: MediaRecorder? = null
    private var isRecording = false
    private var currentFile: File? = null
    private var job: Job? = null
    private val scope = CoroutineScope(Dispatchers.Main + Job())

    private lateinit var storageManager: StorageManager
    private lateinit var prefsManager: PreferencesManager

    // Settings
    private var clipLengthSeconds = 300 // default 5 min
    private var storageLimitGb = 1.0f
    private var currentDuration = 0L

    companion object {
        const val ACTION_START = "ACTION_START"
        const val ACTION_STOP = "ACTION_STOP"
    }

    override fun onCreate() {
        super.onCreate()
        storageManager = StorageManager(this)
        prefsManager = PreferencesManager(this)
        createNotificationChannel()

        // Observe settings changes
        scope.launch {
            prefsManager.clipLengthFlow.collect { minutes ->
                clipLengthSeconds = minutes * 60
            }
        }
        scope.launch {
            prefsManager.storageLimitFlow.collect { gb ->
                storageLimitGb = gb
            }
        }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START -> startRecordingLoop()
            ACTION_STOP -> stopRecordingLoop()
        }
        return START_STICKY
    }

    private fun startRecordingLoop() {
        if (isRecording) return

        startForeground(SERVICE_ID, createNotification("Starting..."),
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE
            } else {
                0
            }
        )
        isRecording = true
        setRecordingState(true)

        job = scope.launch(Dispatchers.IO) {
            while (isActive && isRecording) {
                startNewSegment()
                
                // Monitor duration and stop when limit reached
                currentDuration = 0
                val startTime = System.currentTimeMillis()
                
                while (currentDuration < clipLengthSeconds && isRecording && isActive) {
                    delay(1000)
                    currentDuration = (System.currentTimeMillis() - startTime) / 1000
                    updateDuration(currentDuration)
                    updateNotification("Recording: ${formatTime(currentDuration)}")
                }

                stopCurrentSegment()
                // Storage cleanup
                storageManager.cleanUpStorage(storageLimitGb)
            }
        }
    }

    private fun startNewSegment() {
        try {
            currentFile = getNextFile()
            mediaRecorder = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                MediaRecorder(this)
            } else {
                MediaRecorder()
            }

            mediaRecorder?.apply {
                setAudioSource(MediaRecorder.AudioSource.MIC)
                setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
                setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
                setOutputFile(currentFile?.absolutePath)
                setAudioEncodingBitRate(128000)
                setAudioSamplingRate(44100)
                prepare()
                start()
            }
            // Tag location if enabled (placeholder for now)
            storageManager.saveMetaFile(currentFile!!, "Pending Location") 
        } catch (e: Exception) {
            e.printStackTrace()
            stopRecordingLoop()
        }
    }

    private fun stopCurrentSegment() {
        try {
            mediaRecorder?.stop()
        } catch (e: Exception) {
            // Can happen if stopped immediately after start
        }
        mediaRecorder?.release()
        mediaRecorder = null
    }

    private fun stopRecordingLoop() {
        isRecording = false
        setRecordingState(false)
        job?.cancel()
        stopCurrentSegment()
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    private fun getNextFile(): File {
        val dir = storageManager.getOutputDirectory()
        if (!dir.exists()) dir.mkdirs()
        // Simple timestamped name
        val formatter = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault())
        return File(dir, "REC_${formatter.format(Date())}.m4a")
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Recording Service",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }
    }

    private fun createNotification(content: String): Notification {
        val notificationIntent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, notificationIntent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        
        // Stop action
        val stopIntent = Intent(this, AudioRecorderService::class.java).apply {
            action = ACTION_STOP
        }
        val stopPendingIntent = PendingIntent.getService(
            this, 1, stopIntent, PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Audio Log Recording")
            .setContentText(content)
            .setSmallIcon(R.mipmap.ic_launcher) // Ensure this exists or use built-in
            .setContentIntent(pendingIntent)
            .addAction(android.R.drawable.ic_menu_close_clear_cancel, "Stop", stopPendingIntent)
            .setOngoing(true)
            .build()
    }

    private fun updateNotification(content: String) {
        val manager = getSystemService(NotificationManager::class.java)
        manager.notify(SERVICE_ID, createNotification(content))
    }

    private fun formatTime(seconds: Long): String {
        val hours = seconds / 3600
        val minutes = (seconds % 3600) / 60
        val secs = seconds % 60
        return String.format("%02d:%02d:%02d", hours, minutes, secs)
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        job?.cancel()
        stopCurrentSegment()
    }
}
