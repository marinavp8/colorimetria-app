"use client"
import React, { useState, ChangeEvent } from 'react';
import Result2 from "./Result";
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { GrLinkNext } from "react-icons/gr";
import { Label } from "@/components/ui/label"


interface Result {
    hair: string;
    eyes: string;
    skin: string;
    lips: string;
    colorimetria: string;
    // season: "Verano" | "Otoño" | "Invierno" | "Primavera";
    // subseason: string
}


const ImageUpload = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [result, setResult] = useState<Result | null>(null);

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setSelectedFile(event.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await fetch('http://127.0.0.1:5000/upload', {
                body: formData,
                method: "POST",
            });
            const data = await response.json()
            setResult(data);
        } catch (error) {
            console.error('Error uploading image:', error);
        }
    };

    return (
        <div>
            <div className="flex w-full max-w-sm items-center space-x-2">
                <Input id="picture" type="file" onChange={handleFileChange} />
                <Button onClick={handleUpload}><GrLinkNext className='text-white' />
                </Button>
            </div>


            <div className='text-gray-600 mt-3 ml-1 font-fahkwang'>
                <Label htmlFor="picture">Make sure the photo is clear and the face is visible.</Label>
            </div>

            {/* <h1>Determina tu colorimetría</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Subir Imagen</button> */}
            {result && (
                <div>
                    <p>Cabello: <span style={{ color: result.hair }}>{result.hair}</span></p>
                    <p>Ojos: <span style={{ color: result.eyes }}>{result.eyes}</span></p>
                    <p>Piel: <span style={{ color: result.skin }}>{result.skin}</span></p>
                    <p>Labios: <span style={{ color: result.lips }}>{result.lips}</span></p>
                    <p>Colorimetría: {result.colorimetria}</p>
                    {/* <p>SubColorimetría: {result.subseason}</p> */}
                    {/* <Result2 result={result.subseason} /> */}
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
