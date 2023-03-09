const stars = document.querySelectorAll('.stars i');
const starsNone = document.querySelector('.rating-box');

// ---- ---- Stars ---- ---- //
stars.forEach((star, index1) => {
  star.addEventListener('click', () => {
    stars.forEach((star, index2) => {
      // ---- ---- Active Star ---- ---- //
      index1 >= index2
        ? star.classList.add('active')
        : star.classList.remove('active');
    });
  });
});

function getRating(){
    var rating = 0;
    stars.forEach((star, index1) => {
        if (star.classList.contains('active')){
            rating = index1 + 1;
        }
    }
    );
    document.getElementById('rating_to_be_sent_back').value = rating;
    return true;
}