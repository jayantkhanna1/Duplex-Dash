function change_view_card(){
    document.getElementById("listing").style.display = "block";
    document.getElementById("listing_list_view").style.display = "none";
    document.getElementById("card").classList.add("active");
    document.getElementById("list").classList.remove("active");
}
function change_view_list(){
    document.getElementById("listing").style.display = "none";
    document.getElementById("listing_list_view").style.display = "flex";
    document.getElementById("card").classList.remove("active");
    document.getElementById("list").classList.add("active");
    console.log(document.getElementById("list").classList)
}