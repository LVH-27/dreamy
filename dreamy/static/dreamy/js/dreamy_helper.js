function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
var not_following_button_class = 'btn-success';
var following_button_class = 'btn-warning';



function toggle_follow_button(button) {
  if (button.classList.contains(not_following_button_class)) {
    button.classList.remove(not_following_button_class);
    button.classList.add(following_button_class);
    button.innerHTML = 'Unfollow';
  }
  else {
    button.classList.remove(following_button_class);
    button.classList.add(not_following_button_class);
    button.innerHTML = 'Follow';
  }
}

function update_follow(button) {
  var xhr = new XMLHttpRequest();
  var followee_id = button.id.split('-')[1];
  var following = button.classList.contains(following_button_class);
  if (!following){
    xhr.open('PUT', '/ajax/follow/' + followee_id);
  }
  else {
    xhr.open('PUT', '/ajax/unfollow/' + followee_id);
  }

  // xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.setRequestHeader('X-CSRFToken', csrftoken);
  xhr.onload = function() {
    if (xhr.status === 200) {
      var data = JSON.parse(xhr.responseText);
      if (data['success'] == true) {
        toggle_follow_button(button)
      }
    }
    else {
      alert("Error: " + data['error'])
    }
  }
  xhr.send()
}
