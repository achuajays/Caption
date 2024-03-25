from django.shortcuts import render
from django.http import HttpResponse
import torch
from .image_captioning import predict  # Assuming your image captioning function is in image_captioning.py
from .caption import generater

import os
from django.conf import settings

def caption_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if image_file:
            # Save the uploaded image to a file
            image_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_image.jpg')
            with open(image_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            # Call predict function with the file path
            caption = predict(image_path)  
            
            # Optionally, delete the uploaded image file after processing
            os.remove(image_path)
            caption = remove_text(caption , '<|endoftext|>')
            caption = generater(caption)

            return render(request, 'app/Display.html', {'caption': caption, 'image_url': image_path})
    return render(request, 'app/Display.html')


def remove_text(original_text, text_to_remove):
    # Replace the text to remove with an empty string
    modified_text = original_text.replace(text_to_remove, "")
    return modified_text