(function($, undefined) {
    $.extend({
        jsonRpc: {
            _genericJsonRpc: function(fct_name, params, settings, fct) {
                // Copied from addons/web/static/src/js/core/ajax.js
                // with slightly modifications.
                var data = {
                    jsonrpc: "2.0",
                    method: fct_name,
                    params: params,
                    id: Math.floor(Math.random() * 1000 * 1000 * 1000)
                };
                var xhr = fct(data);
                var result = xhr.then(function(result) {
                    if (result.error !== undefined) {
                        if (result.error.data.arguments[0] !== "bus.Bus not available in test mode") {
                            console.debug(
                                "Server application error\n",
                                "Error code:", result.error.code, "\n",
                                "Error message:", result.error.message, "\n",
                                "Error data message:\n", result.error.data.message, "\n",
                                "Error data debug:\n", result.error.data.debug
                            );
                        }
                        return Promise.reject({type: "server", error: result.error});
                    } else {
                        return result.result;
                    }
                }, function() {
                    //console.error("JsonRPC communication error", _.toArray(arguments));
                    var reason = {
                        type: 'communication',
                        error: arguments[0],
                        textStatus: arguments[1],
                        errorThrown: arguments[2],
                    };
                    return Promise.reject(reason);
                });

                var rejection;
                var promise = new Promise(function (resolve, reject) {
                    rejection = reject;

                    result.then(function (result) {
                        resolve(result);
                    }, function (reason) {
                        var type = reason.type;
                        var error = reason.error;
                        var textStatus = reason.textStatus;
                        var errorThrown = reason.errorThrown;
                        if (type === "server") {
                            reject({message: error, event: $.Event()});
                        } else {
                            var nerror = {
                                code: -32098,
                                message: "XmlHttpRequestError " + errorThrown,
                                data: {
                                    type: "xhr"+textStatus,
                                    debug: error.responseText,
                                    objects: [error, errorThrown],
                                    arguments: [reason || textStatus]
                                },
                            };
                            reject({message: nerror, event: $.Event()});
                        }
                    });
                });

                // FIXME: jsonp?
                promise.abort = function () {
                    rejection({
                        message: "XmlHttpRequestError abort",
                        event: $.Event('abort')
                    });
                    if (xhr.abort) {
                        xhr.abort();
                    }
                };
                return promise;
            },
            
            request: function(url, fct_name, params, settings) {
                // original function is jsonRpc
                settings = settings || {};
                return this._genericJsonRpc(fct_name, params, settings, function(data) {
                    return $.ajax(url, $.extend({}, settings, {
                        url: url,
                        dataType: 'json',
                        type: 'POST',
                        data: JSON.stringify(data),
                        contentType: 'application/json'
                    }));
                });
            }
        }
    });
})(jQuery);
