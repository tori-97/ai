<template>
    <def-modal id="create-bot" ref="modal">
        <template #header>
            <div class="title">Edit Bot</div>
            <div @click="modal?.close" class="close-btn">
                <i class="fas fa-times-circle"></i>
            </div>
        </template>

        <div class="form">
            <div
                class="form-group"
                v-for="key in Object.keys(configuration)"
                :key="key"
            >
                <div class="label">
                    {{
                        key.replaceAll('_', ' ').charAt(0).toLocaleUpperCase() +
                        key.replaceAll('_', ' ').slice(1)
                    }}
                </div>
                <div class="value">
                    <!-- {{ configuration[key as keyof typeof configuration] }} -->
                    <input
                        type="text"
                        :placeholder="(configuration[key as keyof ConfigurationType] as string)"
                        v-model="configuration[key as keyof ConfigurationType]"
                    />
                </div>
            </div>
        </div>

        <template #footer>
            <div class="btn-group">
                <def-btn @click="modal?.close" class="btn">Cancel</def-btn>
                <def-btn @click="update_bot" class="btn">Update</def-btn>
            </div>
        </template>
    </def-modal>
</template>
<script lang="ts" setup>

        import { ref, defineExpose, getCurrentInstance, Ref } from "vue"
        import Modal from "@/components/defaults/defModal.vue"
        import manager from "@/manager";

        const modal = ref<InstanceType<typeof Modal> | null>(null)
        const instance = getCurrentInstance()
        const app = instance?.root.exposed?.app as manager

        const current_bot = ref<string>("")

        interface ConfigurationType{
            name: Ref<string>
            lr: Ref<number>
            hidden_layers: Ref<number>
            gamma: Ref<number>
            discounter_rate: Ref<number>
        }

        const configuration = ref<ConfigurationType>({
            name: ref<string>(""),
            lr: ref<number>(0.0024),
            hidden_layers: ref<number>(43),
            gamma: ref<number>(0.98),
            discounter_rate: ref<number>(20),
        })

        const update_bot = () => {
            let tmp = {}
            Object.assign(tmp, configuration.value)
            app.comunicate('bots', 'bots.update.all', tmp)
        }

        const open = (config: any) => {
            configuration.value = config
            modal.value?.open()
        }

        defineExpose({
            modal,
            open
        })
</script>
<style lang="scss" scoped>
    #create-bot {
        .title {
            &::selection {
                background-color: transparent;
            }
            cursor: default;
        }

        .close-btn {
            cursor: pointer;
        }

        .form {
            width: 32rem;

            padding: 0.6rem;

            display: flex;
            flex-direction: column;
            align-items: center;

            gap: 0.35rem;

            .form-group {
                width: 100%;

                display: flex;
                align-items: center;
                justify-content: center;

                .label {
                    width: 100%;
                    height: 2rem;

                    display: flex;
                    align-items: center;

                    &::selection {
                        background-color: transparent;
                    }

                    cursor: default;
                }

                .value {
                    width: 100%;

                    display: flex;
                    align-items: center;
                    justify-content: flex-end;

                    input,
                    select {
                        border: none;
                        border-radius: 0.35rem;
                        width: 100%;
                        height: 2.2rem;

                        padding: 0.4rem;

                        background-color: #222;
                        color: #bebebe;
                    }
                }
            }
        }

        .btn-group {
            display: flex;
            align-items: center;
            gap: 0.4rem;

            .btn {
                min-width: 6rem;
                background-color: #222;

                &:hover {
                    background-color: orange;
                }

                &:nth-child(1) {
                    background-color: #444;

                    &:hover {
                        background-color: #222;
                        color: #bebebe;
                    }
                }
            }
        }
    }
</style>
