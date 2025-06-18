<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laravel with Vite</title>

</head>
<body>
    <div id="app">
    <h2>Upload and Crop Your Profile Picture</h2>
    <form action="/upload-profile-picture" method="POST" enctype="multipart/form-data">
    @csrf
    <input type="file" id="myFile" name="image">
    <input type="submit" value="Submit">
</form>
    </div>
</body>
</html>
