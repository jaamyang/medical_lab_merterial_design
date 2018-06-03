function password(){
	if(document.getElementById("input").value=="123456"){
    document.getElementById("password").style.display = "none";
    document.getElementById("upload").style.display = "inline";
  }
  else {
    alert("密码错误，请重试");
  }
}
