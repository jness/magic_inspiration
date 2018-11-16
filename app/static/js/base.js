
// execute on page load
function input_storytext(id, name) {

  storytext = document.getElementById('storytext');

  // get current content from textarea
  content = storytext.value;
  content = content + "<a href='/ideas/" + id + "'>" + name + "</a>";

  // update cuntent with item
  storytext.value = content;

  // move cursor back to textarea
  storytext.focus();

};
