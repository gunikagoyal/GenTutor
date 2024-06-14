const firebaseConfig = {
    apiKey: "AIzaSyCYvwWmmWnO2-BPUTNxnJ8_Zxt9nvufmzc",
    authDomain: "aitutor-91225.firebaseapp.com",
    projectId: "aitutor-91225",
    storageBucket: "aitutor-91225.appspot.com",
    messagingSenderId: "58407941688",
    appId: "1:58407941688:web:ab6aa4d7c8363d584458cd",
    measurementId: "G-KXKBKG17P2"
  };
  


  firebase.initializeApp(firebaseConfig);

  const auth = firebase.auth();

  document.getElementById('signup-form').addEventListener('submit', (e) => {
      e.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      auth.createUserWithEmailAndPassword(email, password)
          .then((userCredential) => {
           
              alert('Account created successfully!');
              window.location.href = '../../templates/index.html';
          })
          .catch((error) => {
           
              console.error('Error signing up: ', error);
              alert('Sign up failed. Please check your email and password.');
          });
  });
