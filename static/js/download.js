function downloadImage() {
    // Get image path
    var imgSrc = document.getElementById("generated_img").src;
    console.log(imgSrc)
    // Create a anchor element to download image
    var anchor = document.createElement("a");
    anchor.href = imgSrc;

    // Create image name
    anchor.download = "image.jpg";

    // Auto click to anchor to download
    anchor.click();
}