package com.audiolog.app.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.state_description_range_end
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.audiolog.app.data.PreferencesManager
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    navController: NavController
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val prefs = remember { PreferencesManager(context) }

    val clipLength by prefs.clipLengthFlow.collectAsState(initial = 5)
    val storageLimit by prefs.storageLimitFlow.collectAsState(initial = 1.0f)
    val audioQuality by prefs.audioQualityFlow.collectAsState(initial = "Medium")
    val startOnAppOpen by prefs.startOnAppOpenFlow.collectAsState(initial = false)
    val hapticFeedback by prefs.hapticFeedbackFlow.collectAsState(initial = true)
    val locationTagging by prefs.locationTaggingFlow.collectAsState(initial = false)

    var showLegalDialog by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Settings") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
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
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Text(
                    "Recording",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary
                )
            }

            // Clip Length
            item {
                SettingCard(title = "Clip Length (Minutes)") {
                   Column {
                       Text(
                           text = "$clipLength min",
                           style = MaterialTheme.typography.headlineMedium,
                           modifier = Modifier.align(Alignment.CenterHorizontally)
                       )
                       Slider(
                           value = clipLength.toFloat(),
                           onValueChange = { scope.launch { prefs.setClipLength(it.toInt()) } },
                           valueRange = 1f..30f,
                           steps = 29
                       )
                   }
                }
            }

            // Storage Limit
            item {
                SettingCard(title = "Storage Limit (GB)") {
                    Column {
                        Text(
                            text = String.format("%.1f GB", storageLimit),
                            style = MaterialTheme.typography.headlineMedium,
                            modifier = Modifier.align(Alignment.CenterHorizontally)
                        )
                        Slider(
                            value = storageLimit,
                            onValueChange = { scope.launch { prefs.setStorageLimit(it) } },
                            valueRange = 0.5f..10.0f, // Simplified range
                            steps = 19
                        )
                    }
                }
            }

            // Audio Quality
            item {
                SettingCard(title = "Audio Quality") {
                    Column {
                        listOf("Low", "Medium", "High").forEach { option ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .selectable(
                                        selected = (audioQuality == option),
                                        onClick = { scope.launch { prefs.setAudioQuality(option) } }
                                    )
                                    .padding(vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                RadioButton(
                                    selected = (audioQuality == option),
                                    onClick = { scope.launch { prefs.setAudioQuality(option) } }
                                )
                                Text(
                                    text = option,
                                    modifier = Modifier.padding(start = 16.dp)
                                )
                            }
                        }
                    }
                }
            }

            item {
                Text(
                    "Behavior",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.padding(top = 16.dp)
                )
            }

            item {
                SwitchSetting(
                    title = "Start on App Open",
                    subtitle = "Automatically start recording when app opens",
                    checked = startOnAppOpen,
                    onCheckedChange = { scope.launch { prefs.setStartOnAppOpen(it) } }
                )
            }

            item {
                SwitchSetting(
                    title = "Haptic Feedback",
                    subtitle = "Vibrate on start/stop",
                    checked = hapticFeedback,
                    onCheckedChange = { scope.launch { prefs.setHapticFeedback(it) } }
                )
            }

            item {
                SwitchSetting(
                    title = "Location Tagging",
                    subtitle = "Tag recordings with approximate location",
                    checked = locationTagging,
                    onCheckedChange = { scope.launch { prefs.setLocationTagging(it) } }
                )
            }

            item {
                Text(
                    "Storage Location",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.padding(top = 16.dp)
                )
            }

            item {
                SettingCard(title = "Recording Folder") {
                    Text(
                        text = context.getExternalFilesDir(null)?.absolutePath ?: "Unknown",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color.Gray
                    )
                }
            }

            item {
                Text(
                    "About",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.padding(top = 16.dp)
                )
            }

            item {
                Card(
                    onClick = { showLegalDialog = true },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(Icons.Default.Info, contentDescription = null)
                        Spacer(modifier = Modifier.width(16.dp))
                        Text("Legal & Privacy")
                    }
                }
            }
        }
    }

    if (showLegalDialog) {
        AlertDialog(
            onDismissRequest = { showLegalDialog = false },
            title = { Text("Legal & Privacy") },
            text = {
                Text("The user is responsible for complying with local laws about recording conversations.\n\n" +
                        "Laws may require consent from other parties; in some places, recording private conversations without consent can be illegal.\n\n" +
                        "The app developers and device manufacturer are not responsible for how recordings are used.")
            },
            confirmButton = {
                TextButton(onClick = { showLegalDialog = false }) {
                    Text("Close")
                }
            }
        )
    }
}

@Composable
fun SettingCard(title: String, content: @Composable () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(8.dp))
            content()
        }
    }
}

@Composable
fun SwitchSetting(
    title: String, 
    subtitle: String, 
    checked: Boolean, 
    onCheckedChange: (Boolean) -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(title, style = MaterialTheme.typography.titleMedium)
                Text(subtitle, style = MaterialTheme.typography.bodySmall, color = Color.Gray)
            }
            Switch(checked = checked, onCheckedChange = onCheckedChange)
        }
    }
}
