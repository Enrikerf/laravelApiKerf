<template>
    <div class="card" style="padding: 15px;">
        <div class="card-content">
            <div class="row">
                <div class="col-4">
                    <div class="form-group">
                        <label for="customer">Customer:</label>
                        <typeahead url="/ajax/customers" @input="onCustomer" :initialize="form.customer"/>
                    </div>

                </div>
                <div class="col-4">
                    <div class="form-group">
                        <label for="date">Date:</label><br>
                        <date-picker
                            v-model="form.date"
                            lang="es"
                            format="DD-MM-YYYY"
                            valueType="format"
                            input-class="form-control"
                            :first-day-of-week="1"
                        ></date-picker>
                    </div>
                </div>
                <div class="col-4">
                    <!--<date-picker v-model="form.date"></date-picker>-->
                </div>
            </div>
            <div class="row" style="margin-top: 5rem;">
                <table class="table table-borderes table-stripe table-condensed table-hover">
                    <thead>
                    <tr>
                        <th width="50%">Product</th>
                        <th width="10%">Qty</th>
                        <th width="15%">Price</th>
                        <th width="15%">Total</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="(item, index) in form.items">
                        <td>
                            <typeahead url="/ajax/products"  @input="onProduct(index, $event)" :initialize="item.product"/>
                        </td>
                        <td><input type="number" class="form-control" v-model="item.qty"></td>
                        <td><input type="number" class="form-control" v-model="item.price"></td>
                        <td>{{ item.qty * item.price | currency }}</td>
                        <td><button @click="removeItem(index)" type="button" class="btn btn-danger">DEL</button></td>
                    </tr>
                    </tbody>
                </table>
              <div class="container">
                  <div class="row">
                      <div class="col-9">
                          <button type="button" class="btn btn-primary ml-3" @click="addLine">Nueva Linea</button>

                      </div>
                      <div class="col-3">
                          <h2>TOTAL: {{total | currency}}</h2>
                      </div>
                  </div>
              </div>


            </div>
        </div>
    </div>
</template>

<script>
import DatePicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';
import moment from 'moment';
import Typeahead from "./typeahead/Typeahead";
import Vue from "vue";
export default {
    components: {DatePicker, Typeahead},
    props: {
        id: {
            // default: 1,
            required: true
        }
    },
    data() {
        return {
            form: {
                customer_id: null,
                number: 0,
                date: moment().format('DD-MM-YYYY'),
                items: [
                    {
                        product_id: null,
                        product: 'Producto',
                        descrition: 'Descripcion del producto',
                        qty: 1,
                        price: 0,
                    }
                ]
            }
        }
    },
    computed: {
        total() {
            return this.form.items.reduce((total, item) => {
                return total + Number(item.qty) * Number(item.price)
            }, 0);
        }
    },
    methods:
        {
            addLine() {
                this.form.items.push({
                    product_id: null,
                    product: '',
                    descrition: '',
                    qty: 1,
                    price: 0,
                });
            },
            onCustomer(e) {
                const customer = e.target.value;
                Vue.set(this.$data.form, "customer", customer);
            },
            onProduct(index, e) {
                const product = e.target.value;
                Vue.set(this.form.items[index], "product", product);
                Vue.set(this.form.items[index], "price", product.price);
                //Vue.set(this.form.items[index], "unit_price", product.unit_price);
            },
            removeItem(index) {
                this.form.items.splice(index, 1);
            },
        },
}
</script>

<style scoped>
</style>
