<template>
    <nav>
        <div @click="changeView('home')" class="brand">Ai Trading</div>
        <div class="extend">
            <div @click="changeView('bots')" class="page">Bots</div>
            <div @click="changeView('training')" class="page">Training</div>
        </div>
    </nav>
</template>
<script lang="ts" setup>

    import { ComponentInternalInstance, getCurrentInstance, onMounted } from "vue"
    import { PageInfoType } from "@/utils/types";

    let instance: ComponentInternalInstance;

    onMounted(()=> {
        instance = getCurrentInstance() as ComponentInternalInstance

    })
    
    const changeView = (to: string) => {
        if(!instance.parent?.exposed) return false


        let save_page_info = window.localStorage.getItem("page-info") as string

        if ( save_page_info ){
            const page_info = JSON.parse(save_page_info) as PageInfoType
            page_info.current_view = to
            window.localStorage.setItem("page-info", JSON.stringify(page_info))
        }

        instance.parent.exposed.current_view.value = to as string
    }
</script>
<style lang="scss" scoped>
    nav {
        width: 100%;
        height: 3.2rem;
        min-height: 3.2rem;

        display: flex;
        align-items: center;
        justify-content: space-between;

        background-color: #222;
        box-shadow: 0px 0px 3px 0px #333;

        padding: 0.4rem;

        .brand {
            font-size: 1.22rem;
            font-weight: 500;
            padding: 0.2rem;

            cursor: pointer;
        }

        .extend { 
            display: flex;
            align-items: center;

            .page { 
                padding: .4rem;
                margin: .2rem;

                &:hover {
                    background-color: #111;
                    box-shadow: 0px 0px 4px 0px #222;

                    border-radius: .2rem;
                    cursor: pointer;

                }
            }
        }

    }
</style>
