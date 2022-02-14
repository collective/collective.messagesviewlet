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

  function show_unclosed_messages() {
    var m_uids = Cookies.get('messagesviewlet');
    if (typeof m_uids === "undefined") {
      // no cookie set, so we show all messages
      $("#messagesviewlet > div, #localmessagesviewlet > div").show();
      return;
    }

    m_uids = m_uids.split("|");
    $("#messagesviewlet > div, #localmessagesviewlet > div").each(function(){
      // we show only messages that are not in cookie as "closed messages"
      if ($.inArray($(this).attr('id'), m_uids) == -1) $(this).show();
    });
  }
  show_unclosed_messages();
});
