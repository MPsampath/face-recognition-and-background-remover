<?php

namespace App\Http\Controllers;

use Illuminate\Http\Client\Response;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;
use Intervention\Image\Facades\Image;

class ImageUpload extends Controller
{
    public function uploadProfile(Request $request)
    {
        try {
       // Validate the uploaded image
        $request->validate([
            'image' => 'required|image|mimes:jpeg,png,jpg,gif',
        ]);

        $original_image_name = 'original_' . time() . $request->file('image')->getClientOriginalExtension();
        dd($original_image_name);
        // Get the full path to the image
        $path = Storage::disk('public')->put('processed/' . $original_image_name, $request->file('image'));
        dd($path);

          // Command to execute the Python script inside the virtual environment
        $pythonPath = '/home/prasana-sampath/myenv/bin/python3'; // Path to your Python executable in the virtual environment
        $scriptPath = base_path('python-script/face_recognition.py'); // Path to your Python script
        $outputPath = '/home/prasana-sampath/Pictures/output.png';
        $process = new Process([$pythonPath, $scriptPath, $path, '']);
        
        $process->run();
        
        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }
        
         if (!$process->isSuccessful()) {
        return response()->json([
            'error' => 'Script execution failed',
            'stderr' => $process->getErrorOutput(),
        ], 500);
    }

    // Get the binary image data
    $imageData = $process->getOutput();

    // Define the path to save in public directory
    $filename = 'processed_' . time() . '.png';
    $publicPath = public_path('processed/' . $filename);

    // Ensure the directory exists
    if (!file_exists(dirname($publicPath))) {
        mkdir(dirname($publicPath), 0755, true);
    }

    // Save the image
    file_put_contents($publicPath, $imageData);

    // Return the image as response
    return new Response($imageData, 200, [
        'Content-Type' => 'image/png',
        'Content-Disposition' => 'inline; filename="' . $filename . '"',
    ]);
        
        } catch (\Throwable $th) {
           dd($th);
        }
    }
}



