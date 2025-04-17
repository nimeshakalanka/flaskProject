const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const gallery = document.getElementById('gallery');


navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
.then(stream => {
    video.srcObject = stream;

    setInterval(() => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        const dataURL = canvas.toDataURL('image/jpeg', 0.5);  

        const formData = new FormData();
        formData.append('image', dataURL);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Uploaded Image URL:', data.image_url);

            const imgElement = document.createElement('img');
            imgElement.src = data.image_url;
            imgElement.style.width = "200px";
            imgElement.style.margin = "10px";
            gallery.prepend(imgElement);
        })
        .catch(error => console.error('Upload error:', error));

    }, 5000);
})
.catch(err => {
    console.error("Camera error: ", err);
});
