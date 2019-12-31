from PIL.ImagePath import Path
from django.shortcuts import render, redirect
import glob
import os

from app.forms import GetImageForm

import pickle

from PIL import Image

from app.models import ImageCompress

from huffman_coding.tree import HuffmanTree


def home(request):
    return render(request, 'app/home.html')


def compression(request):
    if request.method == 'POST':
        p_form = GetImageForm(request.POST, request.FILES)

        if p_form.is_valid():
            p_form.save()
            compressed()
            return redirect('compress')


    else:
        p_form = GetImageForm()

    context = {
        'p_form': p_form
    }

    return render(request, 'app/compress.html', context)


def compressed():
    list_of_files = glob.glob('E:/PROGRAMMING/DJango/sample project/media/photos/*')  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    img = Image.open(latest_file)
    data = img.getdata()

    data_list = []

    for tup in list(data):
        for val in tup:
            data_list.append(val)

    huffman_tree = HuffmanTree(data=data_list)
    huffman_tree.create_tree()
    root = huffman_tree.root
    compressed_file_data = huffman_tree.get_compressed_file(key=2)

    meta_data = compressed_file_data[0]
    bit_array = compressed_file_data[1]

    with open(r"E:\PROGRAMMING\DJango\sample project\media\photos\image_meta.dat", 'wb') as fp:
        pickle.dump(meta_data, fp)

    with open(r"E:\PROGRAMMING\DJango\sample project\media\photos\image_compressed.bin", 'wb') as fp:
        fp.write(bit_array)


