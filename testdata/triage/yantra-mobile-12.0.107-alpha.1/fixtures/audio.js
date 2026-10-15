import {useAudioRecorder} from 'expo-audio'; const recorder = useAudioRecorder(preset); await recorder.prepareToRecordAsync(); recorder.record();
