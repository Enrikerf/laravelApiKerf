<template>
    <div :class="[isOpen ? 'typeahead typeahead-open' : 'typeahead']">
        <div class="typeahead-inner">
            <div
                class="form-control typeahead-selected"
                :tabindex="tabindex"
                ref="toggle"
                @click="onToggle"
                @keydown="onKey"
            >
                <div class="tx-flex">
                    <span>{{selectedText}}</span>
                </div>
            </div>

            <transition name="fade" mode="out-in">
                <div class="typeahead-dropdown" v-show="isOpen">
                    <div class="typeahead-input_wrap">
                        <input
                            type="text"
                            class="typeahead-input"
                            autocomplete="off"
                            placeholder="Buscar..."
                            ref="search"
                            @blur="onBlur"
                            @input="onSearch"
                            @keydown.esc="onEsc"
                            @keydown.up="onUpKey"
                            @keydown.down="onDownKey"
                            @keydown.enter="onEnterKey"
                        />
                    </div>
                    <ul class="typeahead-list">
                        <li class="typeahead-item" v-for="(result, index) in results" :key="result.id">
                            <a
                                :class="['typeahead-link', selectIndex === index ? 'typeahead-active':'']"
                                @mousedown.prevent="select(result)"
                                @mouseover.prevent="onMouse(index)"
                            >
                                <div class="tx-flex tx-flex-col">
                                    <span class="tx-font-black tx-uppercase">{{result.name}}</span>
                                    <span class="tx-text-xs tx-uppercase tx-text-my-comision">{{result.subname}}</span>
                                </div>
                            </a>
                        </li>
                    </ul>
                </div>
            </transition>
        </div>
    </div>
</template>
<script type="text/javascript">
    import Vue from "vue";
    import axios from "axios";
    export default {
        props: {
            initialize: {
                default: null
            },
            show: {
                default: true
            },
            url: {
                required: true
            },
            tabindex: {
                default: 0
            },
        },
        data() {
            return {
                selectIndex: -1,
                isOpen: false,
                search: "",
                results: [{text: "text"}],
                showm: false,
            };
        },
        computed: {
            selectedText() {
                return this.initialize && this.initialize.text
                    ? this.initialize.text
                    : "Escriba o haga clic para seleccionar";
            },
            subText() {
                return this.initialize && this.initialize.description
                    ? this.initialize.description
                    : "";
            }
        },
        methods: {
            onToggle() {
                if (this.show && !this.showm) {
                    if (this.isOpen) {
                        this.isOpen = false;
                    } else {
                        this.open();
                    }
                }
            },
            modal()
            {
                this.showm = !this.showm;
                if(this.modal)
                {
                    this.$emit("modal");
                }
            },
            onKey(e) {
                const KeyCode = e.KeyCode || e.which;
                if (!e.shiftKey && KeyCode !== 9 && !this.isOpen) {
                    this.open();
                }
            },
            open() {
                this.fetchData("");
                this.isOpen = true;
                this.$nextTick(() => {
                    this.$refs.search.focus();
                });
            },
            fetchData(q) {
                axios
                    .get(this.url, {
                        params: {
                            query: q
                        }
                    })
                    .then(res => {
                        Vue.set(this.$data, "results", res.data);
                    });
            },
            onBlur() {
                this.close();
            },
            onEsc() {
                this.close();
            },
            close() {
                this.results = [];
                this.isOpen = false;
                this.search = "";
                this.selectIndex = -1;
            },
            onSearch(e) {
                const q = e.target.value;
                this.selectIndex = 0;
                this.fetchData(q);
            },
            onUpKey(e) {
                if (this.selectIndex > 0) {
                    this.selectIndex--;
                }
            },
            onDownKey(e) {
                if (this.results.length - 1 > this.selectIndex) {
                    this.selectIndex++;
                }
            },
            onEnterKey() {
                const found = this.results[this.selectIndex];
                if (found) {
                    this.select(found);
                }
            },
            select(result) {
                this.$emit("input", {
                    target: {
                        value: result
                    }
                });
                this.close();
            },
            onMouse(index) {
                this.selectIndex = index;
            }
        }
    };
</script>
<style scoped>
</style>
