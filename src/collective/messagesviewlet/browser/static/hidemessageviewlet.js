$(document).ready(function(){
  $(".close-button").click(function(){
    var m_uids = Cookies.get('messagesviewlet');
    var m_uid = $(this).parent().attr('id');
    if (typeof m_uids === "undefined") {m_uids = m_uid;}
    else {m_uids += "|" + m_uid;}
    Cookies.set('messagesviewlet', m_uids, { expires: 30 });
    $(this).parent().hide();
    });
});
