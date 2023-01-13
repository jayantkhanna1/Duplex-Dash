
var tag = 0
function open_user_details_modal(){
    if(tag == 0){
        document.getElementById("user_info_modal").style.display = "flex";
        tag = 1;
    }
    else{
        document.getElementById("user_info_modal").style.display = "none";
        tag = 0;
    }

}