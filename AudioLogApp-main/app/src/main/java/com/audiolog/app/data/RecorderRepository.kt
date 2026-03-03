package com.audiolog.app.data

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.io.File

object RecorderRepository {
    private val _isRecording = MutableStateFlow(false)
    val isRecording: StateFlow<Boolean> = _isRecording.asStateFlow()

    private val _currentDurationSeconds = MutableStateFlow(0L)
    val currentDurationSeconds: StateFlow<Long> = _currentDurationSeconds.asStateFlow()

    private val _storageUsedBytes = MutableStateFlow(0L)
    val storageUsedBytes: StateFlow<Long> = _storageUsedBytes.asStateFlow()

    private val _filesList = MutableStateFlow<List<File>>(emptyList())
    val filesList: StateFlow<List<File>> = _filesList.asStateFlow()

    fun setRecordingState(isRecording: Boolean) {
        _isRecording.value = isRecording
    }

    fun updateDuration(seconds: Long) {
        _currentDurationSeconds.value = seconds
    }

    fun updateStorageUsage(bytes: Long) {
        _storageUsedBytes.value = bytes
    }
    
    fun updateFilesList(files: List<File>) {
        _filesList.value = files
    }
}
