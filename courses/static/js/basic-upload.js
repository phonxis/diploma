$(function () {
  // var for message from server
  var loaded_data;

  // кнопка загрузки файла
  uploadButton = $('<button/>')
    .addClass('btn btn-primary')
    .prop('disabled', true)
    .text('Processing...')
    .on('click', function () {
      var $this = $(this),
        data = $this.data();
      $this
        .off('click')
        .text('Uploading...')
        .on('click', function () {
          $this.remove();
          data.abort();
        });
      data.submit().always(function () {
        $this.remove();
      });
    });

  // вывод сообщения
  function addMessage(text, extra_tags) {
    var message = $('<div class="alert alert-dismissible '+extra_tags+'">'+text+'</div>').hide();
    $("#messages").append(message);
    message.fadeIn(500);

    setTimeout(function() {
      message.fadeOut(500, function() {
        message.remove();
      });
    }, 3000);
  }

  $('#fileupload').fileupload({
    dataType: 'json',
    autoUpload: false,
    paramName: 'data_field',
    done: function (e, data) {
      loaded_data = data.result;
      //console.log(data.result)
      $.each(data.result.django_messages, function (i, item) {
        //console.log(item);
        addMessage(item.message, item.extra_tags);
      });
    }
  }).on('fileuploadadd', function (e, data) {
    data.context = $('<div/>').appendTo('#files');
    $.each(data.files, function (index, file) {
      var node = $('<p/>')
        .append($('<span/>').text(file.name));
      if (!index) {
        node
          .append('<br>')
          .append(uploadButton.clone(true).data(data));
      }
      node.appendTo(data.context);
    });
  }).on('fileuploadprocessalways', function (e, data) {
    var index = data.index,
      file = data.files[index],
      node = $(data.context.children()[index]);
    if (file.preview) {
      node
        .prepend('<br>')
        .prepend(file.preview);
    }
    if (file.error) {
      node
        .append('<br>')
        .append($('<span class="text-danger"/>').text(file.error));
    }
    if (index + 1 === data.files.length) {
      data.context.find('button')
        .text('Upload')
        .prop('disabled', !!data.files.error);
    }
  }).prop('disabled', !$.support.fileInput)
    .parent().addClass($.support.fileInput ? undefined : 'disabled');
});