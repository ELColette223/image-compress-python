from flask import Flask, request, jsonify, Response
from PIL import Image
import io
import base64
import threading
import time
import platform
import cpuinfo

app = Flask(__name__)

def compress_image(image_bytes, format, quality, timeout_seconds=10):
    """Compresses an image, maintaining the format and adjusting the quality, with a timeout."""
    start_time = time.time()
    # Open the image from the given bytes
    image = Image.open(io.BytesIO(image_bytes))
    # Create a BytesIO object to store the compressed image
    image_io = io.BytesIO()

    # Create a timer to close the image after the specified timeout
    timer = threading.Timer(timeout_seconds, image.close)
    timer.start()

    try:
        # Save the image with the specified format and quality
        if format.upper() == 'JPEG':
            image.save(image_io, format=format, quality=quality, optimize=True)
        else:
            image.save(image_io , format=format, optimize=True)
        # Move the file pointer to the beginning of the BytesIO object
        image_io.seek(0)

        compressed_size = len(image_io.getvalue())
        original_size = len(image_bytes)

        # Check if the compressed size is smaller than the original size
        while compressed_size >= original_size and quality > 0:
            # Decrease the quality and compress again
            quality -= 10
            image_io.truncate(0)
            image_io.seek(0)

            if format.upper() == 'JPEG':
                image.save(image_io, format=format, quality=quality, optimize=True)
            else:
                image.save(image_io, format=format, optimize=True)

            # Move the file pointer to the beginning of the BytesIO object
            image_io.seek(0)
            compressed_size = len(image_io.getvalue())

    finally:
        # Cancel the timer if the image is saved successfully
        timer.cancel()

    end_time = time.time()  # Capturing end time
    execution_time = end_time - start_time  # Calculating execution time

    # Return the compressed image as bytes and execution time
    return image_io.read(), execution_time

def get_processor_name():
    info = cpuinfo.get_cpu_info()
    return info['brand_raw']

@app.errorhandler(404)
def not_found(e):
    return """
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        <title>Image Compression Service</title>
    </head>
    <body style="padding:20px;">
        <h1>404 - Page Not Found</h1>
        <p>The page you are looking for does not exist.</p>
    </body>
    </html>
    """

@app.route('/')
def index():
    index_page = """
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        <title>Image Compression Service</title>
    </head>
    <body style="padding:20px;">
        <h1>Image Compression Service</h1>
        <p> how to compress an image using this service:</p>
        <br><ol>
            <li> Use the cURL command with localfile:</li><br>
<pre>
curl --location 'http://localhost:5000/compress?quality=Fat' \</pre><pre>
--form 'file=@"/path/to/your/image.jpg"'
</pre>
            <br><li> Or use the cURL base64 command:</li><br>
<pre>
curl --location 'http://localhost:5000/compress?quality=Fat' \ </pre><pre>
--header 'Content-Type: application/json' \ </pre><pre>
--data '{"image":"iVBORw0KGgoAAAANSUhEUgAAAvUAAAKWCAYAAADJImZ5AAAAAXNSR0IArs4c6QAAAAR..."}'
</pre>
        </ol>
        <br><p>The service have three compression quality options:</p>
        <ul>
            <li>Light (90% quality)</li>
            <li>Medium (67% quality)</li>
            <li>High (48% quality)</li>
            <li>Fat (15% quality)</li>
        </ul>
    </body>
    </html>
    """
    return index_page

@app.errorhandler(405)
def method_not_allowed(e):
    return """
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
        <title>Image Compression Service</title>
    </head>
    <body style="padding:20px;">
        <h1>405 - Method Not Allowed</h1>
        <p>The method you are using is not allowed on this endpoint.</p>
    </body>
    </html>
    """

@app.route('/compress', methods=['POST'])
def compress():
    image_bytes = None
    format = None
    
    image_compression_quality = request.args.get('quality')

    if image_compression_quality == "Light":
        selected_quality = 90
    elif image_compression_quality == "Medium":
        selected_quality = 67
    elif image_compression_quality == "High":
        selected_quality = 48
    elif image_compression_quality == "Fat":
        selected_quality = 15
    else:
        selected_quality = 80
    
    if 'file' in request.files:
        # If a file is uploaded, read its bytes and determine the format
        file = request.files['file']
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        format = image.format
    elif 'image' in request.json:
        # If an image is provided in the JSON payload, decode the base64 data and determine the format
        image_data = request.json['image']
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        format = image.format
    else:
        # If no image is provided, return an error response
        return jsonify({'error': 'No image provided'}), 400

    try:
        # Compress the image with the specified format and quality
        compressed_image_bytes, execution_time = compress_image(image_bytes, format, selected_quality, timeout_seconds=10)
    except Exception as e:
        # If there is a timeout or error during compression, return an error response
        return jsonify({'error': 'Processing timeout or error', 'message': str(e)}), 500

    # Calculate the original size, compressed size, and compression ratio
    original_size = len(image_bytes)
    compressed_size = len(compressed_image_bytes)
    compression_ratio_percent = 100 - (compressed_size * 100 / original_size)

    # Set the response headers
    headers = {
        'Content-Type': f'image/{format.lower()}',
        'X-Original-Size': str(original_size),
        'X-Compressed-Size': str(compressed_size),
        'X-Compression-Ratio-Percent': f'{compression_ratio_percent:.2f}%',
        'X-Compression-Quality': str(selected_quality),
        'X-Compression-Method': 'Pillow',
        'X-Compression-Execution-Time': f'{execution_time:.4f} seconds',
        'X-Compression-Platform': platform.system(),
        'X-Compression-Platform-Version': platform.version(),
        'X-Processor-Name': platform.processor(),
        'X-Processor-Processor-Name': get_processor_name(),
    }

    if 'file' in request.files:
        # If a file was uploaded, return the compressed image as a response with the headers
        return Response(compressed_image_bytes, headers=headers)
    elif 'image' in request.json:
        # If an image was provided in the JSON payload, return the compressed image as a JSON response with the headers
        response_image = base64.b64encode(compressed_image_bytes).decode('utf-8')
        return jsonify({'compressed_image': response_image}), 200, headers

if __name__ == '__main__':
    try:
        # Run the Flask app in debug mode with threading enabled
        app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f'Error: {e}')
        app.logger.error(e)
