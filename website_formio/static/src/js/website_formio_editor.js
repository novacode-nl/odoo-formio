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
        popup_title: _t("Add a Form"),

        select_formio_builder: function (previewMode, value) {
            var self = this;
            return rpc.query({
                model: 'formio.builder',
                method: 'search_read',
                args: [[['public', '=', true], ['state', '=', 'CURRENT']],['uuid', 'display_name_full']],
                context: self.options.recordInfo.context,
            }).then(function (formio_builders) {
                var def = wUtils.prompt({
                    'id': self.popup_template_id,
                    'window_title': self.popup_title,
                    'select': _t("Form"),
                    'init': function (field) {
                        var $add = $('<div/>', {'class': 'form-group row mt-4 mb0'})
                            .append($('<div/>', {'class': 'col-md-12 text-left'})
                                    .append($('<em>' +
                                              _t("IMPORTANT: in case the Form won't appear, add the affected (website page) Model and Field into configuration of the \"Website Editor Unsanitize HTML Field\" (in menu: Website / Configuration).") +
                                              '</em></strong>')));
                        this.$dialog.find('form div.form-group').after($add);
                        return _.map(formio_builders, function (formio_builder) {
                            return [formio_builder['uuid'], formio_builder['display_name_full']];
                        });
                    },
                });
                def.then(function (result) {
                    var form_iframe = self.$target.find('.formio_form_iframe_container iframe'),
                        iframe_src = '/formio/public/form/create/' + result.val;
                    form_iframe.attr("src", iframe_src);
                    iFrameResize({}, '.formio_form_embed');
                });
            });
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
