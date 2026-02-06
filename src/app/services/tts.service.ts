import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface TTSRequest {
    text: string;
    lang: string;
    voice?: string;
    gender?: string;
    speed?: string;
}

@Injectable({
    providedIn: 'root'
})
export class TtsService {
    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    /**
     * Generate TTS audio from text
     * @param text - Text to convert to speech
     * @param lang - Language code (e.g., en-US, ur-PK)
     * @param gender - Voice gender (male/female)
     * @param speed - Speech speed (normal/slow/fast)
     * @param voice - Optional specific voice name
     * @returns Observable<Blob> - MP3 audio as blob
     */
    generateTTS(
        text: string,
        lang: string,
        gender: string = 'female',
        speed: string = 'normal',
        voice?: string
    ): Observable<Blob> {
        const url = `${this.apiUrl}/tts`;
        const body: TTSRequest = { text, lang, gender, speed, voice };

        return this.http.post(url, body, {
            responseType: 'blob',
            headers: new HttpHeaders({
                'Content-Type': 'application/json'
            })
        });
    }

    /**
     * Get available voices from backend
     */
    getAvailableVoices(): Observable<any> {
        const url = `${this.apiUrl}/voices`;
        return this.http.get(url);
    }
}
