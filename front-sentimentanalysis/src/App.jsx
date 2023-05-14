import {
    Container,
    FormControl,
    FormLabel,
    TextareaAutosize,
    Button,
} from "@mui/material";
import { useState, useEffect } from "react";
import AudioRecorder from "./components/AudioRecorder";

const App = () => {
    const [audioDisabled, setAudioDisabled] = useState(true);
    const [audioChunks, setAudioChunks] = useState(null);
    const [isRecording, setIsRecording] = useState(false);
    const [text, setText] = useState("");
    const [textDisabled, setTextDisabled] = useState(true);

    useEffect(() => {
        if (text !== "") {
            setTextDisabled(false);
        } else {
            setTextDisabled(true);
        }
    }, [text]);

    useEffect(() => {
        if (audioChunks !== null) {
            if (isRecording === false) {
                setAudioDisabled(false);
            }
        } else {
            setAudioDisabled(true);
        }
    }, [audioChunks]);

    const handleSendAudio = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("file", audioBlob);

        fetch("http://localhost:5000/upload_audio", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => console.log(data.message))
            .catch((error) => console.error(error));
    };

    const handleSendText = () => {
        const formData = new FormData();
        formData.append("text", text);
        
        fetch("http://localhost:5000/upload_text", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => console.log(data.message))
            .catch((error) => console.error(error));
    };

    return (
        <Container maxWidth="md">
            <h1 className="font-bold text-xl py-3">Sentiment Analysis</h1>
            <FormControl className="w-full">
                <FormLabel className="mt-10" htmlFor="audio">
                    Audio
                </FormLabel>
                <AudioRecorder
                    audioChunks={audioChunks}
                    setAudioChunks={setAudioChunks}
                    isRecording={isRecording}
                    setIsRecording={setIsRecording}
                />

                <Button variant="contained" disabled={audioDisabled} onClick={(e) => handleSendAudio(e)}>
                    Send Audio
                </Button>
                <FormLabel className="mt-10" htmlFor="Text">
                    Text
                </FormLabel>
                <TextareaAutosize
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    className="min-h-[5rem] mb-3 p-2 bg-gray-100 rounded-md w-full"
                />
                <Button variant="contained" disabled={textDisabled} onClick={(e) => handleSendText(e)}>
                    Send Text
                </Button>
            </FormControl>
        </Container>
    );
};

export default App;
