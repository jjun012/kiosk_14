function validateForm() {
    var dateOfBirth = document.getElementById('dateOfBirth').value;
    var phoneNumber = document.getElementById('phoneNumber').value;

    //pass를 이용한 성인 인증은 추후에 구현 예정

    window.location.href = "http://127.0.0.1:5000/";

    return false;
}
