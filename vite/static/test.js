const { axios } = require('axios')

axios.get('https://mimoso.herokuapp.com/api/v1/users')
.then(function (response) {
    // handle success
    console.log(response);
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .then(function () {
    // always executed
  });