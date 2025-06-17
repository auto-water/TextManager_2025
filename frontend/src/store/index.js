import { createStore } from 'vuex'
import userModule from './modules/user'
import articleModule from './modules/article'
import categoryModule from './modules/category'

// 持久化 state 的一个简单方法 (可选，但推荐)
// 你也可以使用 vuex-persistedstate 插件
const loadState = () => {
  try {
    const serializedState = localStorage.getItem('vuex_state');
    if (serializedState === null) {
      return undefined;
    }
    return JSON.parse(serializedState);
  } catch (err) {
    console.error("Could not load state from localStorage", err);
    return undefined;
  }
};

const saveState = (state) => {
  try {
    const serializedState = JSON.stringify(state);
    localStorage.setItem('vuex_state', serializedState);
  } catch (err) {
    console.error("Could not save state to localStorage", err);
  }
};

const store = createStore({
  modules: {
    user: userModule,
    article: articleModule,
    category: categoryModule
  },
})

// 如果有持久化的数据，选择性地恢复到对应的模块中
const persistedState = loadState();
if (persistedState && persistedState.user) {
  // 只恢复需要的字段，而不是整个状态对象
  if (persistedState.user.token) {
    store.state.user.token = persistedState.user.token;
  }
  if (persistedState.user.currentUser) {
    store.state.user.currentUser = persistedState.user.currentUser;
  }
}

// 每次 state 变化时保存到 localStorage
store.subscribe((mutation, state) => {
  // 只持久化特定模块或整个 state
  // 例如，只持久化 user 模块的 token 和 currentUser
  const stateToPersist = {
    user: {
      token: state.user.token,
      currentUser: state.user.currentUser
    }
    // 如果需要，可以添加其他模块的持久化数据
  };
  saveState(stateToPersist);
});


export default store