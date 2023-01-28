<template>
    <container>
        <side-panel ref="side_panel" />
        <container-content>
            <top-bar ref="topbar" />
            <graph ref="graph" />
        </container-content>

        <create-new-bot-modal ref="create_new_bot_modal" />
        <start-training-modal ref="start_training_modal" />
    </container>
</template>
<script lang="ts" setup>
    import Container from '@/components/AppContainer.vue'
    import ContainerContent from '@/components/AppContainerContent.vue'
    import SidePanel from '@/components/TrainingView/SidePanel.vue'
    import TopBar from '@/components/TrainingView/TopBar.vue'
    import Graph from '@/components/TrainingView/GraphElement.vue'

    import CreateNewBotModal from '@/components/TrainingView/popups/CreateNewBotModal.vue'
    import StartTrainingModal from '@/components/TrainingView/popups/StartTrainingModal.vue'

    import { ref, defineExpose } from 'vue'

    let create_new_bot_modal = ref<InstanceType<
        typeof CreateNewBotModal
    > | null>(null)

    let start_training_modal = ref<InstanceType<
        typeof StartTrainingModal
    > | null>(null)

    let graph = ref<InstanceType<typeof Graph> | null>(null)
    const side_panel = ref<InstanceType<typeof SidePanel> | null>(null)
    const topbar = ref<InstanceType<typeof TopBar> | null>(null)

    defineExpose({
        create_new_bot_modal,
        start_training_modal,
        graph,
        side_panel,
        topbar
    })
</script>
<style lang="scss" scoped></style>
