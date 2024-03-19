# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

{
    'name': 'Forms',
    'summary': 'Form Builder for internal, portal, website and embedded forms, to collect any information you need for your business.',
    'version': '16.0.10.18',
    'license': 'LGPL-3',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'live_test_url': 'https://demo16.novacode.nl',
    'category': 'Forms/Forms',
    'depends': [
        'base',
        'mail',
        'portal',
        'web',
    ],
    'application': True,
    'installable': True,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'data': [
        # the ordering is important
        'data/formio_builder_js_options_data.xml',
        'data/formio_default_asset_css_data.xml',
        'data/formio_version_data.xml',
        'data/formio_asset_data.xml',
        'data/formio_extra_asset_data.xml',
        'data/formio_default_version_data.xml',
        'data/ir_config_param.xml',
        'data/ir_cron_data.xml',
        'data/mail_activity_data.xml',
        'data/mail_template_data.xml',
        # translations
        'data/formio_translations_sources.xml',
        'data/formio_translations_nl.xml',
        'data/formio_translations_nl_BE.xml',
        'data/formio_translations_pt_BR.xml',
        'data/formio_translations_zh_CN.xml',
        # security
        'security/formio_security.xml',
        'security/ir_model_access.xml',
        'security/ir_rule.xml',
        # views
        'views/formio_builder_js_options_views.xml',
        'views/formio_builder_translation_views.xml',
        'views/formio_builder_views.xml',
        'views/formio_extra_asset_views.xml',
        'views/formio_form_views.xml',
        'views/formio_res_model_views.xml',
        'views/formio_translation_source_views.xml',
        'views/formio_translation_views.xml',
        'views/formio_version_github_tag_views.xml',
        'views/formio_version_translation_views.xml',
        'views/formio_version_views.xml',
        'views/formio_menu.xml',
        'views/res_config_settings_views.xml',
        'views/res_lang_views.xml',
        'views/ir_actions_views.xml',
        'views/ir_attachment_views.xml',
        'views/mail_activity_views.xml',
        # formio templates
        'views/formio_builder_templates.xml',
        'views/formio_form_templates.xml',
        'views/formio_portal_templates.xml',
        'views/formio_public_templates.xml',
        # wizards
        'wizard/formio_version_github_checker_wizard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # builder
            'formio/static/src/css/formio_builder.css',
            'formio/static/src/js/views/formio_builder.xml',
            'formio/static/src/js/views/formio_builder.js',
            # form
            'formio/static/src/css/formio_form.css',
            'formio/static/src/js/views/formio_form.xml',
            'formio/static/src/js/views/formio_form.js',
            # misc
            'formio/static/lib/iframe-resizer/iframeResizer.min.js'
        ],
        'web.assets_frontend': [
            'formio/static/src/css/formio_portal_form.css',
            'formio/static/lib/iframe-resizer/iframeResizer.min.js',
            'formio/static/src/js/formio_form_container.js'
        ],
        'web.assets_common': [
            'formio/static/lib/iframe-resizer/iframeResizer.min.js',
        ],
    },
    'demo': [
        'data/formio_demo_data.xml',
    ],
    'images': [
        'static/description/banner.gif',
    ]
}
