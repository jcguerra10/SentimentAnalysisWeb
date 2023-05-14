import { Button } from "@mui/material";
import React, { useState } from "react";

const AudioRecorder = ({
    audioChunks,
    setAudioChunks,
    isRecording,
    setIsRecording,
}) => {
    const [mediaRecorder, setMediaRecorder] = useState(null);

    const handleStartRecording = async () => {
        setAudioChunks([]);
        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
        });
        const recorder = new MediaRecorder(stream);
        setMediaRecorder(recorder);

        recorder.ondataavailable = (e) => {
            setAudioChunks((prev) => [...prev, e.data]);
        };

        recorder.start();
        setIsRecording(true);
    };

    const handleStopRecording = () => {
        mediaRecorder.stop();

        mediaRecorder.stream.getTracks().forEach((track) => track.stop());
        setIsRecording(false);
    };

    const handleClear = (e) => {
        e.preventDefault();
        setAudioChunks(null);
    };

    return (
        <div className="flex gap-3 py-4">
            <Button
                variant="contained"
                color="success"
                disabled={isRecording}
                onClick={handleStartRecording}>
                Start
            </Button>
            <Button
                variant="contained"
                color="error"
                disabled={!isRecording}
                onClick={handleStopRecording}>
                Stop
            </Button>
            {audioChunks && (
                <Button variant="text" color="secondary" onClick={(e) => handleClear(e)}>
                    clear
                </Button>
            )}
        </div>
    );
};

export default AudioRecorder;
