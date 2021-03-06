import cv2
import pyramids
import heartrate
import preprocessing
import eulerian

def get_heartrate(filename):
    # Frequency range for Fast-Fourier Transform
    freq_min = 1
    freq_max = 1.8

    # Preprocessing phase
    hr = -1 # Valor por defecto

    video_frames, frame_ct, fps = preprocessing.read_video(filename)

    # Build Laplacian video pyramid

    lap_video = pyramids.build_video_pyramid(video_frames)

    amplified_video_pyramid = []

    for i, video in enumerate(lap_video):
        if i == 0 or i == len(lap_video)-1:
            continue

        # Eulerian magnification with temporal FFT filtering

        result, fft, frequencies = eulerian.fft_filter(video, freq_min, freq_max, fps)
        lap_video[i] += result

        # Calculate heart rate

        hr = heartrate.find_heart_rate(fft, frequencies, freq_min, freq_max)

    return hr, filename
