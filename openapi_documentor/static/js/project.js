/* Project specific Javascript goes here. */
function get_current_uuid(url=null) {
    if(url === null ){
        url = window.location.href;
    }
    matches = url.match(/((\w{4,12}-?)){5}/gm);
    return (matches && matches.length) ? matches[0] : null;
}

$(document).ready(function(){
    var $openapiSelector = $(".openapi-select");
    var currentUUID = get_current_uuid();
    $openapiSelector.select2({
        width: '400px',
        placeholder: 'Type api name or tag',
        cacheDataSource: [],
        ajax: {
            url: '/api/openapis/',
            data: function (params) {
                return {search: params.term, format: 'json'};
            },
            processResults: function (data) {
                return {
                    results: $.map(data.results, function (obj) {
                        return {
                            id: obj.id,
                            text: obj.title,
                            selected: (currentUUID === obj.id)
                        }
                    })
                };
            }
        }
    });

    $openapiSelector.on("select2:select", function (e) {
        var docid = e.target.value;
        if(docid !== currentUUID)
            window.location.href = '/openapis/'+docid
    });

    if(!!currentUUID) {
        $.ajax(
            {type: 'GET', url: '/api/openapis/' + currentUUID}
        ).then(function (data) {
            var option = new Option(data.title, data.id, true, true);
            $openapiSelector.append(option).trigger('change')
        });
    }
});

