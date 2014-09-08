


detect_android = ->
    ua = navigator.userAgent.toLowerCase();
    isAndroid = ua.indexOf("android") > -1; //&& ua.indexOf("mobile");
    return isAndroid




class Upload
    constructor: ->
        @obj = $('#id_file')
        @android = detect_android()
        @button = $('#upload')
        @form = $('form')
        @init()



    init: ->
        if @android
           @init_adroid()
        else
            @init_ios()

        @obj.on('change',$.proxy(@file_event,@))

    init_adroid: ->
        @button.hide()

    init_ios: ->
        @obj.hide()
        @button.on('click', =>
            @obj.click()
            )
    file_event: ->
        @form.submit()

    #init_events: ->
$ ->
    new Upload()
    $('.alert').delay(1000).fadeOut('slow')