/** @odoo-module **/

import { registry } from "@web/core/registry";
import { KeepLast } from "@web/core/utils/concurrency";
import { useBus, useService } from "@web/core/utils/hooks";
import { ActionMenus } from "@web/search/action_menus/action_menus";
import { Layout } from "@web/search/layout";
import { useModel } from "@web/views/model";
import { RelationalModel } from "@web/views/relational_model";
import { standardViewProps } from "@web/views/standard_view_props";
import { FormArchParser } from "@web/views/form/form_arch_parser";
import { FormCompiler } from "@web/views/form/form_compiler";
import { FormControlPanel } from "@web/views/form/control_panel/form_control_panel";
import { useSetupView } from "@web/views/view_hook";
import { Component, onWillStart, useEffect, useRef, useState } from "@odoo/owl";

export class BuilderController extends Component {
    setup() {
        this.router = useService("router");
        // this.action = useService("action");
        this.orm = useService("orm");
        this.ui = useService("ui");
        this.state = useState({
            isDisabled: false,
        });
        useBus(this.ui.bus, "resize", this.render);

        this.archInfo = this.props.archInfo;
        const activeFields = this.archInfo.activeFields;

        this.beforeLoadResolver = null;
        const beforeLoadProm = new Promise((r) => {
            this.beforeLoadResolver = r;
        });
        const fields = this.props.fields;
        const mode = 'edit';

        // props: model
        this.model = useModel(
            RelationalModel,
            {
                resModel: 'formio.builder',
                resId: this.props.resId,
                fields: fields,
                activeFields,
                viewMode: "formio_builder",
                rootType: "record",
                mode,
                beforeLoadProm,
                component: this,
            },
            {
                ignoreUseSampleModel: true,
            }
        );

        // props: model
        this.display = { ...this.props.display };
        this.display.controlPanel = true;

        // useSetupView({
        //     rootRef: useRef("root"),
        //     // beforeLeave: () => this.beforeLeave(),
        //     // beforeUnload: (ev) => this.beforeUnload(ev),
        //     getLocalState: () => {
        //         const { data, metaData } = this.model;
        //         console.log(data);
        //         return { data, metaData };
        //     },
        // });

        onWillStart(async () => {
            // needed to wait on useModel (data loading)
            this.beforeLoadResolver();
        });

        useEffect(() => {
            this.updateURL();
        });
    }
    
    updateURL() {
        this.router.pushState({ id: this.model.root.resId || undefined });
    }
}


BuilderController.template = "formio.BuilderView";
BuilderController.components = { ActionMenus, Layout };
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
    multiRecord: false,
    searchMenuTypes: [],
    ControlPanel: FormControlPanel, // especially for breadcrumbs
    Controller: BuilderController,
    Renderer: BuilderRenderer,
    Model: RelationalModel,
    ArchParser: FormArchParser, // to parse fields for formio_builder view (type)
    Compiler: FormCompiler, // to parse fields for formio_builder view (type)
    
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
