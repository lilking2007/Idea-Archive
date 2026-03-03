package com.audiolog.app.data

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")

class PreferencesManager(private val context: Context) {

    companion object {
        val CLIP_LENGTH_MINUTES = intPreferencesKey("clip_length_minutes")
        val STORAGE_LIMIT_GB = floatPreferencesKey("storage_limit_gb")
        val AUDIO_QUALITY = stringPreferencesKey("audio_quality")
        val START_ON_APP_OPEN = booleanPreferencesKey("start_on_app_open")
        val HAPTIC_FEEDBACK = booleanPreferencesKey("haptic_feedback")
        val LOCATION_TAGGING = booleanPreferencesKey("location_tagging")
        val STORAGE_PATH = stringPreferencesKey("storage_path")
    }

    val clipLengthFlow: Flow<Int> = context.dataStore.data.map { it[CLIP_LENGTH_MINUTES] ?: 5 } // Default 5 mins for safety, user can change
    val storageLimitFlow: Flow<Float> = context.dataStore.data.map { it[STORAGE_LIMIT_GB] ?: 1.0f } // Default 1GB
    val audioQualityFlow: Flow<String> = context.dataStore.data.map { it[AUDIO_QUALITY] ?: "Medium" }
    val startOnAppOpenFlow: Flow<Boolean> = context.dataStore.data.map { it[START_ON_APP_OPEN] ?: false }
    val hapticFeedbackFlow: Flow<Boolean> = context.dataStore.data.map { it[HAPTIC_FEEDBACK] ?: true }
    val locationTaggingFlow: Flow<Boolean> = context.dataStore.data.map { it[LOCATION_TAGGING] ?: false }
    val storagePathFlow: Flow<String> = context.dataStore.data.map { it[STORAGE_PATH] ?: "" }

    suspend fun setClipLength(minutes: Int) {
        context.dataStore.edit { it[CLIP_LENGTH_MINUTES] = minutes }
    }

    suspend fun setStorageLimit(gb: Float) {
        context.dataStore.edit { it[STORAGE_LIMIT_GB] = gb }
    }

    suspend fun setAudioQuality(quality: String) {
        context.dataStore.edit { it[AUDIO_QUALITY] = quality }
    }

    suspend fun setStartOnAppOpen(enabled: Boolean) {
        context.dataStore.edit { it[START_ON_APP_OPEN] = enabled }
    }

    suspend fun setHapticFeedback(enabled: Boolean) {
        context.dataStore.edit { it[HAPTIC_FEEDBACK] = enabled }
    }

    suspend fun setLocationTagging(enabled: Boolean) {
        context.dataStore.edit { it[LOCATION_TAGGING] = enabled }
    }

    suspend fun setStoragePath(path: String) {
        context.dataStore.edit { it[STORAGE_PATH] = path }
    }
}
