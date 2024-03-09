/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useBus, useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { useModel } from "@web/model/model";
import { RelationalModel } from "@web/model/relational_model/relational_model";
import { extractFieldsFromArchInfo } from "@web/model/relational_model/utils";
// import { formView } from "@web/views/form/form_view";
import { standardViewProps } from "@web/views/standard_view_props";
import { ViewButton } from "@web/views/view_button/view_button";
import { FormArchParser } from "@web/views/form/form_arch_parser";
import { FormCompiler } from "@web/views/form/form_compiler";
import { Component, useEffect, useState } from "@odoo/owl";

// if (formView.icon === undefined) {
//     formView.icon = "fa fa-file";
// }

export class BuilderController extends Component {
    setup() {
        this.router = useService("router");
        this.orm = useService("orm");
        this.state = useState({
            isDisabled: false,
        });
        this.ui = useService("ui");
        useBus(this.ui.bus, "resize", this.render);

        this.archInfo = this.props.archInfo;
        const activeFields = this.archInfo.activeFields;
        const fields = this.props.fields;
        const mode = 'edit';

        const beforeFirstLoad = async () => {
            const { activeFields, fields } = extractFieldsFromArchInfo(
                this.archInfo,
                this.props.fields
            );
            this.model.config.activeFields = activeFields;
            this.model.config.fields = fields;
        };

        this.model = useState(useModel(this.props.Model, this.modelParams, { beforeFirstLoad }));

        this.display = { ...this.props.display };

        useEffect(() => {
            this.updateURL();
        });
    }
    
    updateURL() {
        this.router.pushState({ id: this.model.root.resId || undefined });
    }

    get modelParams() {
        let mode = this.props.mode || "edit";
        if (!this.canEdit && this.props.resId) {
            mode = "readonly";
        }
        return {
            config: {
                resModel: this.props.resModel,
                resId: this.props.resId || false,
                fields: this.props.fields,
                activeFields: {}, // will be generated after loading sub views (see willStart)
                isMonoRecord: true,
                mode,
                context: this.props.context,
            },
            state: this.props.state?.modelState,
        };
    }
}

BuilderController.template = "formio.BuilderView";
BuilderController.components = {
    Layout,
    ViewButton,
};
BuilderController.props = {
    ...standardViewProps,
    Model: Function,
    Renderer: Function,
    Compiler: Function,
    archInfo: Object,
};

export class BuilderRenderer extends Component {
    setup() {
        super.setup();
    }
}

export const BuilderView = {
    type: "formio_builder",
    display_name: "Form Builder",
    icon: "fa fa-rocket",
    // multiRecord: true, // when false it shows viewButtons
    // multiRecord: false, // ideally to show viewButtons
    searchMenuTypes: [],
    Controller: BuilderController,
    Renderer: BuilderRenderer,
    ArchParser: FormArchParser,
    Model: RelationalModel,
    Compiler: FormCompiler,
    
    props: (genericProps, view) => {
        const { ArchParser } = view;
        const { arch, relatedModels, resModel } = genericProps;
        const archInfo = new ArchParser().parse(arch, relatedModels, resModel);
        let modelParams = genericProps.state;
        if (!modelParams) {
            const { arch,  resModel, fields, context} = genericProps;
            modelParams = {
                context: context,
                fields: fields,
            };
        }
        return {
            ...genericProps,
            Model: view.Model,
            Renderer: view.Renderer,
            Compiler: view.Compiler,
            archInfo,
        };
    },
};

registry.category("views").add('formio_builder', BuilderView);
