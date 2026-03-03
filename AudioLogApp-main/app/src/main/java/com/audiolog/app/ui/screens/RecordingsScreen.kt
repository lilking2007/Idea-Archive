package com.audiolog.app.ui.screens

import android.media.MediaPlayer
import android.net.Uri
import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.LockOpen
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Stop
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.audiolog.app.data.Recording
import com.audiolog.app.data.StorageManager
import kotlinx.coroutines.launch
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RecordingsScreen(
    navController: NavController
) {
    val context = LocalContext.current
    val storageManager = remember { StorageManager(context) }
    var recordings by remember { mutableStateOf<List<Recording>>(emptyList()) }
    val scope = rememberCoroutineScope()
    
    // Playback state
    var currentPlayingFile by remember { mutableStateOf<File?>(null) }
    var isPlaying by remember { mutableStateOf(false) }
    val mediaPlayer = remember { MediaPlayer() }

    // Load data
    LaunchedEffect(Unit) {
        recordings = storageManager.getRecordings()
    }

    fun stopPlayback() {
        if (mediaPlayer.isPlaying) {
            mediaPlayer.stop()
        }
        mediaPlayer.reset()
        isPlaying = false
        currentPlayingFile = null
    }

    fun playRecording(recording: Recording) {
        val file = recording.file
        if (currentPlayingFile == file && isPlaying) {
            stopPlayback()
        } else {
            stopPlayback()
            try {
                mediaPlayer.setDataSource(context, Uri.fromFile(file))
                mediaPlayer.prepare()
                mediaPlayer.start()
                isPlaying = true
                currentPlayingFile = file
                mediaPlayer.setOnCompletionListener {
                    stopPlayback()
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Error playing file", Toast.LENGTH_SHORT).show()
                e.printStackTrace()
                stopPlayback()
            }
        }
    }
    
    fun delete(recording: Recording) {
        if (recording.isLocked) {
           Toast.makeText(context, "Cannot delete locked file", Toast.LENGTH_SHORT).show() 
           return
        }
        // Stop if playing this file
        if (currentPlayingFile == recording.file) {
            stopPlayback()
        }
        
        scope.launch {
            storageManager.deleteRecording(recording.file)
            recordings = storageManager.getRecordings()
        }
    }
    
    fun toggleLock(recording: Recording) {
        scope.launch {
            val success = storageManager.toggleLock(recording.file)
            if (success) {
                recordings = storageManager.getRecordings()
            } else {
                Toast.makeText(context, "Failed to toggle lock", Toast.LENGTH_SHORT).show()
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Recordings") },
                navigationIcon = {
                    IconButton(onClick = { 
                        stopPlayback()
                        navController.popBackStack() 
                    }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .padding(padding)
                .fillMaxSize(),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            if (recordings.isEmpty()) {
                item {
                    Box(modifier = Modifier.fillMaxSize().padding(32.dp), contentAlignment = Alignment.Center) {
                        Text(
                            "No recordings found",
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.secondary
                        )
                    }
                }
            } else {
                items(recordings) { recording ->
                    RecordingItemKeyed(
                        recording = recording,
                        isPlaying = (currentPlayingFile == recording.file && isPlaying),
                        onPlay = { playRecording(recording) },
                        onDelete = { delete(recording) },
                        onToggleLock = { toggleLock(recording) }
                    )
                }
            }
        }
    }
    
    DisposableEffect(Unit) {
        onDispose {
            mediaPlayer.release()
        }
    }
}

@Composable
fun RecordingItemKeyed(
    recording: Recording, 
    isPlaying: Boolean,
    onPlay: () -> Unit,
    onDelete: () -> Unit,
    onToggleLock: () -> Unit
) {
    Card(
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (recording.isLocked) MaterialTheme.colorScheme.surfaceVariant else MaterialTheme.colorScheme.surface
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onPlay) {
                Icon(
                    if (isPlaying) Icons.Default.Stop else Icons.Default.PlayArrow,
                    contentDescription = if (isPlaying) "Stop" else "Play",
                    tint = MaterialTheme.colorScheme.primary
                )
            }
            
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 8.dp)
            ) {
                val dateFormat = SimpleDateFormat("dd MMM yyyy, HH:mm", Locale.getDefault())
                val dateStr = try {
                    dateFormat.format(Date(recording.timestamp))
                } catch (e: Exception) { "Unknown Date" }
                
                Text(
                    text = dateStr,
                    style = MaterialTheme.typography.titleMedium
                )
                
                // Format size
                val kb = recording.size / 1024.0
                val mb = kb / 1024.0
                val sizeStr = if (mb >= 1) String.format("%.1f MB", mb) else String.format("%.0f KB", kb)
                
                Text(
                    text = "$sizeStr • ${recording.location}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            IconButton(onClick = onToggleLock) {
                Icon(
                    if (recording.isLocked) Icons.Default.Lock else Icons.Default.LockOpen,
                    contentDescription = if (recording.isLocked) "Unlock" else "Lock",
                    tint = if(recording.isLocked) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            IconButton(onClick = onDelete) {
                Icon(
                    Icons.Default.Delete,
                    contentDescription = "Delete",
                    tint = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}
