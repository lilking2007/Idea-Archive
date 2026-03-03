package com.audiolog.app.data

import android.content.Context
import android.os.Environment
import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

data class Recording(
    val file: File,
    val name: String,
    val timestamp: Long,
    val size: Long,
    val durationText: String, // Approximate or formatted
    val isLocked: Boolean,
    val location: String = "Unknown"
)

class StorageManager(private val context: Context) {

    private val defaultDirName = "AudioLog"

    fun getOutputDirectory(): File {
        // Use app-specific external storage which doesn't require extra permissions for writing
        val baseDir = context.getExternalFilesDir(null)
        val dir = File(baseDir, defaultDirName)
        if (!dir.exists()) {
            dir.mkdirs()
        }
        return dir
    }

    fun createNewFile(): File {
        val dir = getOutputDirectory()
        val timestamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(Date())
        return File(dir, "REC_$timestamp.m4a")
    }

    fun saveMetaFile(audioFile: File, location: String) {
        val metaFile = File(audioFile.parent, audioFile.nameWithoutExtension + ".meta")
        try {
            metaFile.writeText(location)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun getMetaLocation(audioFile: File): String {
        val metaFile = File(audioFile.parent, audioFile.nameWithoutExtension + ".meta")
        return if (metaFile.exists()) {
            metaFile.readText()
        } else {
            "Unknown"
        }
    }

    suspend fun getRecordings(): List<Recording> = withContext(Dispatchers.IO) {
        val dir = getOutputDirectory()
        val files = dir.listFiles { file -> file.extension == "m4a" } ?: return@withContext emptyList()
        
        files.map { file ->
            val isLocked = file.name.startsWith("LOCKED_")
            val location = getMetaLocation(file)
            Recording(
                file = file,
                name = file.name,
                timestamp = file.lastModified(),
                size = file.length(),
                durationText = "?", // Calculating actual duration requires MediaMetadataRetriever, which is slow for list. 
                isLocked = isLocked,
                location = location
            )
        }.sortedByDescending { it.timestamp }
    }

    suspend fun cleanUpStorage(limitGb: Float) {
        val limitBytes = (limitGb * 1024 * 1024 * 1024).toLong()
        val dir = getOutputDirectory()
        val files = dir.listFiles { file -> file.extension == "m4a" } ?: return

        // Calculate total size
        var totalSize = files.sumOf { it.length() }

        if (totalSize > limitBytes) {
            // Sort by oldest first
            val sortedFiles = files.sortedBy { it.lastModified() }
            
            for (file in sortedFiles) {
                if (file.name.startsWith("LOCKED_")) continue // Skip locked

                val size = file.length()
                if (file.delete()) {
                    // Also delete meta
                    val meta = File(file.parent, file.nameWithoutExtension + ".meta")
                    if (meta.exists()) meta.delete()
                    
                    totalSize -= size
                    if (totalSize <= limitBytes) break
                }
            }
        }
    }

    fun toggleLock(file: File): Boolean {
        val parent = file.parentFile
        val newName = if (file.name.startsWith("LOCKED_")) {
            file.name.removePrefix("LOCKED_")
        } else {
            "LOCKED_" + file.name
        }
        val newFile = File(parent, newName)
        val success = file.renameTo(newFile)
        
        // Rename meta file too if exists
        if (success) {
            val oldMeta = File(parent, file.nameWithoutExtension + ".meta")
            if (oldMeta.exists()) {
                oldMeta.renameTo(File(parent, newFile.nameWithoutExtension + ".meta"))
            }
        }
        return success
    }

    fun deleteRecording(file: File) {
        val meta = File(file.parent, file.nameWithoutExtension + ".meta")
        if (meta.exists()) meta.delete()
        file.delete()
    }
}
