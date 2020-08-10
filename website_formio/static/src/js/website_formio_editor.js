odoo.define('website_formio_editor', function (require) {
    'use strict';

    var core = require('web.core');
    var rpc = require('web.rpc');
    var options = require('web_editor.snippets.options');
    var wUtils = require('website.utils');
    var Dialog = require('web.Dialog');
    var _t = core._t;

    options.registry.website_formio_editor = options.Class.extend({
        popup_template_id: "editor_new_formio_form_popup",
        popup_title: _t("Add a Form.io Form"),

        select_formio_builder: function (previewMode, value) {
            var self = this;
            var def = wUtils.prompt({
                'id': this.popup_template_id,
                'window_title': this.popup_title,
                'select': _t("Form"),
                'init': function (field, dialog) {
                    return rpc.query({
                        model: 'formio.builder',
                        method: 'name_search',
                        args: ['', [['public', '=', true]]],
                        context: self.options.recordInfo.context,
                    }).then(function (data) {
                        $(dialog).find('.btn-primary').prop('disabled', !data.length);
                        return data;
                    });
                },
            });
            def.then(function (result) {
                var form_iframe = self.$target.find('.formio_form_iframe_container iframe'),
                    iframe_src = '/formio/public/form/create/' + result.val;
                form_iframe.attr("src", iframe_src);
            });
            return def;
        },

        onBuilt: function () {
            var self = this;
            this._super();
            this.select_formio_builder('click').guardedCatch(function () {
                self.getParent()._onRemoveClick($.Event( "click" ));
            });
        },
    });
});
