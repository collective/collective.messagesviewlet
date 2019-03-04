$(document).ready(function(){
  $("#messagesviewlet .close-button").click(function(){
    var m_uids = $.cookie('messagesviewlet');
    var m_uid = $(this).parent().attr('id');
    if (typeof m_uids === "undefined") {m_uids = m_uid;}
    else {m_uids += "|" + m_uid;}
    $.cookie('messagesviewlet', m_uids, { expires: 60 });
    $(this).parent().hide();
    });
});
