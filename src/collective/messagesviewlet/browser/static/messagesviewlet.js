jQuery(document).ready(function ($) {
  function handler(event) {
    var m_uids = Cookies.get('messagesviewlet');
    var m_uid = $(this).parent().attr('id');
    if (typeof m_uids === "undefined") {m_uids = m_uid;}
    else {m_uids += "|" + m_uid;}
    Cookies.set('messagesviewlet', m_uids, { expires: 60 });
    $(this).parent().hide();
    }
  $("#messagesviewlet .close-button").bind("click",{}, handler);
  $("#localmessagesviewlet .close-button").bind("click",{}, handler);
});
