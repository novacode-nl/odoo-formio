// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

$(document).ready(function() {
    var uuid = document.getElementById('form_uuid').value,
        base_url = window.location.protocol + '//' + window.location.host,
        formio_uuid = '/formio/form/' + uuid,
        schema_url = formio_uuid + '/schema/',
        options_url = formio_uuid + '/options/',
        submission_url = formio_uuid + '/submission/',
        title_url = formio_uuid + '/title/',
        paperformat_url = formio_uuid + '/paperformat/',
        schema = {},
        options = {};

    async function getPDF() {
        var component = await getComponent();
        var submission = await getSubmission();
        var options = await getOptions();
        var config = await getConfig();
        var exporter = new FormioExport(component, submission, options);

        exporter.toPdf(config);
    }

    async function getConfig() {
        var title = await getTitle();
        var paperformat = await getPaperformat();
        return {
            download: true,
            filename: title + '.pdf',
            margin: [paperformat['margin_top'], paperformat['margin_right'], paperformat['margin_bottom'], paperformat['margin_left']],
            html2canvas: {
                scale: 5,
                logging: false
            },
            jsPDF: {
                orientation: paperformat['orientation'],
                unit: paperformat['format']['unit'],
                format: paperformat['format']['size']
            }
        };
    }

    function getTitle() {
        return $.jsonRpc.request(title_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                return result
            }
        });
    }

    function getPaperformat() {
        return $.jsonRpc.request(paperformat_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                return JSON.parse(result)
            }
        });
    }

    async function getComponent() {
        var title = await getTitle();
        return $.jsonRpc.request(schema_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                var schema = JSON.parse(result);
                return {
                            type: 'form',
                            title: title,
                            display: 'form',
                            components: schema['components']
                        }
            }
        });
    }

    function getSubmission() {
        return $.jsonRpc.request(submission_url, 'call', {}).then(function(result) {
            if (!$.isEmptyObject(result)) {
                return {'data': JSON.parse(result)};
            }
        });
    }

    function getOptions() {
        return $.jsonRpc.request(options_url, 'call', {}).then(function(_options) {
            var options = JSON.parse(_options);
            var hooks = {
                'addComponent': function(container, comp, parent) {
                    if (comp.hasOwnProperty('component') && comp.component.hasOwnProperty('data') &&
                        comp.component.data.hasOwnProperty('url') && !$.isEmptyObject(comp.component.data.url)) {
                        comp.component.data.url = base_url.concat(comp.component.data.url, '/', uuid);
                    }
                    return container;
                }
            };
            options['hooks'] = hooks;
            return options
        });
    }

    $("#formio_print").click(getPDF);
});
