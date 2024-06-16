// Elements
const el = {
    signUpHome: document.getElementById('sign-up'),
    signInHome: document.getElementById('sign-in'),
    btnHome: document.querySelector('.btn-back'),
    pageMain: document.querySelector('.main'),
    pageHome: document.querySelector('.home'),
    pageSignUp: document.querySelector('.sign-up'),
    formArea: document.querySelector('.form-area'),
    sideSignLeft: document.querySelector('.signup-left'),
    sideSignRight: document.querySelector('.signup-right'),
    formSignUp: document.querySelector('.form-area-signup'),
    formSignIn: document.querySelector('.form-area-signin'),
    linkUp: document.querySelector('.link-up'),
    linkIn: document.querySelector('.link-in'),
    btnSignUp: document.querySelector('.btn-up'),
    btnSignIn: document.querySelector('.btn-in'),
    labels: document.getElementsByTagName('label'),
    inputs: document.getElementsByTagName('input'),
    popup: document.getElementById('popup'),
    closePopup: document.getElementById('close-popup'),
  };
  
  // ADD Events
  // Show the page Sign Up
  el.signUpHome.addEventListener('click', function(e) {
    showSign(e, 'signup');
  });
  el.linkUp.addEventListener('click', function(e) {
    showSign(e, 'signup');
  });
  
  // Show the page sign in
  el.signInHome.addEventListener('click', function(e) {
    showSign(e, 'signin');
  });
  el.linkIn.addEventListener('click', function(e) {
    showSign(e, 'signin');
  });
  
  // Show the page Home
  el.btnHome.addEventListener('click', showHome);
  
  // Handle form submission for sign up
  el.formSignUp.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();
    showPopup();
  });
  
  // Close popup and go to home
  el.closePopup.addEventListener('click', closePopup);

  el.formSignIn.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault(); 
    
    var phone = document.getElementById('phone-in').value;
    var password = document.getElementById('password-in').value;
 
    if (phone.trim() === '' || password.trim() === '') {
      alert('전화번호와 비밀번호를 입력하세요.');
      return;
    }
   
    showPopup('로그인이 완료되었습니다!'); // 팝업 표시
  setTimeout(function() {
    window.location.href = 'home.html'; // 홈페이지로 리디렉션
  }, 1500); // 1.5초 후에 리디렉션
});
  
  // Functions Events
  // function to show screen Home
  function showHome(event) {
    setTimeout(function() {
      el.sideSignLeft.style.padding = '0';
      el.sideSignLeft.style.opacity = '0';
      el.sideSignRight.style.opacity = '0';
      el.sideSignRight.style.backgroundPositionX = '235%';
  
      el.formArea.style.opacity = '0';
      setTimeout(function() {
        el.pageSignUp.style.opacity = '0';
        el.pageSignUp.style.display = 'none';
        for (input of el.inputs) {
          input.value = '';
        }
      }, 900);
    }, 100);
  
    setTimeout(function() {
      el.pageHome.style.display = 'flex';
    }, 1100);
    
    setTimeout(function() {
      el.pageHome.style.opacity = '1';
    }, 1200);
  }
  
  // function to show screen Sign up/Sign in
  function showSign(event, sign) {
    if (sign === 'signup') {
      el.formSignUp.style.display = 'flex';
      el.formSignIn.style.opacity = '0';
      setTimeout(function() {
        el.formSignUp.style.opacity = '1';
      }, 100);
      el.formSignIn.style.display = 'none';
    } else {
      el.formSignIn.style.display = 'flex';
      el.formSignUp.style.opacity = '0';
      setTimeout(function() {
        el.formSignIn.style.opacity = '1';
      }, 100);
      el.formSignUp.style.display = 'none';
    }
  
    el.pageHome.style.opacity = '0';
    setTimeout(function() {
      el.pageHome.style.display = 'none';
    }, 700);
    
    setTimeout(function() {
      el.pageSignUp.style.display = 'flex';
      el.pageSignUp.style.opacity = '1';
      
      setTimeout(function() {
        el.sideSignLeft.style.padding = '20px';
        el.sideSignLeft.style.opacity = '1';
        el.sideSignRight.style.opacity = '1';
        el.sideSignRight.style.backgroundPositionX = '230%';
  
        el.formArea.style.opacity = '1';
      }, 10);
    }, 900);
  }
  
  // function to show popup
  function showPopup() {
    el.popup.style.display = 'block';
  }
  
  // function to close popup
  function closePopup() {
    el.popup.style.display = 'none';
    showHome();
  }
  
  // Behavior of the inputs and labels
  for (input of el.inputs) {
    input.addEventListener('keydown', function() {
      this.labels[0].style.top = '10px';
    });
    input.addEventListener('blur', function() {
      if (this.value === '') {
        this.labels[0].style.top = '25px';
      }
    });
  }
  