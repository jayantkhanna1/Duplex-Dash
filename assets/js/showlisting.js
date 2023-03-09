function changeImage(clickedImage,id) {
    var newImageSrc = clickedImage;
    var headerImage = document.querySelector('.header-image');
    headerImage.src = newImageSrc;
    
    // Remove active class from all images
    for (var i = 1; i <= 6; i++) {
        try{
            document.getElementById('outer_img_'+i).classList.remove('active');
        }
        catch(err){
        }
        
    }
    // Add active class to clicked image
    document.getElementById('outer_img_'+id).classList.add('active');

  }