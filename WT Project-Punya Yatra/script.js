
function checkUsername(){
    const uname = document.getElementById("username").value;
    const errorText = document.getElementById("userError")
    if(uname.length<6){
        errorText.style.display = "block";
        return false;
    }
    else{
        errorText.style.display="none";
        return true;
    }
}


function checkPass() {
    const pass = document.getElementById("password").value;
    const passError = document.getElementById("passError");

    if (pass.length < 8) {
        passError.innerText = "Password too small";
        passError.style.display = "block";
        return false;
    }
    if (!/[a-z]/.test(pass)) {
        passError.innerText = "At least one lowercase letter is needed";
        passError.style.display = "block";
        return false;
    }
    if (!/[A-Z]/.test(pass)) {
        passError.innerText = "At least one uppercase letter is needed";
        passError.style.display = "block";
        return false;
    }
    if (!/\d/.test(pass)) {
        passError.innerText = "At least one digit is needed";
        passError.style.display = "block";
        return false;
    }
    if (!/[~`!@#$%^&*()_+\-|\[\]{}<>\\\/]/.test(pass)) {
        passError.innerText = "At least one special character is needed";
        passError.style.display = "block";
        return false;
    }
    passError.style.display = "none";
    return true;
}



function checkRePass() {
    let password = document.getElementById("password").value;
    let rePassword = document.getElementById("rePassword").value;
    let message = document.getElementById("passAndconfirm");
    let eyebutton = document.getElementById("eye-icon");

    if (password.length > 0 && rePassword.length > 0) {
        if (password !== rePassword) {
            message.style.display = "block";
            message.innerText = "Passwords do not match!";
            eyebutton.style.transform="translateY(-115%)";
            return false;
        } else {
            message.style.display = "none";
            eyebutton.style.transform="translateY(-50%)";
            return true;
        }
    }
    else{
        message.style.display = "none";
        eyebutton.style.transform="translateY(-50%)";
        return false;
    }
}


function togglePassword() {
    let passwordInput = document.getElementById("rePassword");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}


function ageSelect(){
    let ageBlock = document.getElementById("age");
    
    for(i=18;i<101;i++){
        let option = document.createElement("option");
        option.value = i;
        option.innerText = i;
        ageBlock.appendChild(option);
    }
}
ageSelect()


function validateForm() {
    let isUsernameValid = checkUsername();
    let isPasswordValid = checkPass();
    let isRePasswordValid = checkRePass();

    if (!isUsernameValid || !isPasswordValid || !isRePasswordValid) {
        return false;
    }
    return true;
}




