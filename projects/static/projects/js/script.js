function addInput() {
  var imagesInput = document.getElementById("imagesInput");
  // Create a new container div
  var div = document.createElement("div");
  div.classList.add("d-flex", "gap-2");

  // Create a new input element
  var newInput = document.createElement("input");
  newInput.className = "form-control";
  newInput.type = "file";
  newInput.accept = "image/*";
  newInput.name = "pictures";
  newInput.required = true;

  // Create delete button
  var delButton = document.createElement("button");
  delButton.type = "button";
  delButton.classList.add("btn", "btn-xs", "btn-danger");
  delButton.onclick = () => {
    div.remove();
  };

  // create span for trash image
  var trashSpan = document.createElement("span");
  trashSpan.classList.add("fa-solid", "fa-trash-can");

  // Append span to the del button
  delButton.appendChild(trashSpan);

  // Append del button to the div
  div.appendChild(newInput);
  div.appendChild(delButton);

  // Append the new input element to the imagesInput div
  imagesInput.appendChild(div);
}
