<template>
  <div class="admin-user-manager">
    <h2>用户管理</h2>

    <div v-if="isLoading" class="loading-indicator">加载用户列表中...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <table v-if="users.length > 0 && !isLoading" class="user-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>用户名</th>
          <th>邮箱</th>
          <th>状态</th>
          <th>管理员</th>
          <th>加入日期</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>
            <span :class="['status-badge', user.is_frozen ? 'frozen' : (user.is_active ? 'active' : 'inactive')]">
              {{ user.is_frozen ? '已冻结' : (user.is_active ? '活跃' : '不活跃') }}
            </span>
          </td>
          <td>{{ user.is_staff ? '是' : '否' }}</td>
          <td>{{ formatDate(user.date_joined) }}</td>
          <td class="user-actions">
            <button @click="toggleFreezeUser(user)" :disabled="actionLoading === user.id" class="action-btn freeze-btn">
              {{ actionLoading === user.id && currentAction === 'freeze' ? '处理中...' : (user.is_frozen ? '解冻' : '冻结') }}
            </button>
            <button @click="toggleAdminStatus(user)" :disabled="actionLoading === user.id" class="action-btn admin-toggle-btn">
               {{ actionLoading === user.id && currentAction === 'admin' ? '处理中...' : (user.is_staff ? '撤销管理' : '设为管理') }}
            </button>
            <!-- 删除用户操作需谨慎 -->
            <button @click="deleteUser(user.id)" :disabled="actionLoading === user.id" class="action-btn delete-btn">
               {{ actionLoading === user.id && currentAction === 'delete' ? '删除中...' : '删除' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="!isLoading && !error">暂无用户数据。</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

const actionLoading = ref(null); // Store user ID being acted upon
const currentAction = ref(''); // 'freeze', 'admin', 'delete'

const users = computed(() => store.getters['user/allUsers']);
const isLoading = computed(() => store.state.user.isLoading); // Assuming user module has isLoading
const error = computed(() => store.getters['user/authError']); // Or a specific adminError

onMounted(() => {
  store.dispatch('user/fetchAllUsers');
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

const toggleFreezeUser = async (user) => {
  actionLoading.value = user.id;
  currentAction.value = 'freeze';
  try {
    await store.dispatch('user/updateUserAdmin', {
      userId: user.id,
      data: { is_frozen: !user.is_frozen }
    });
    // Optimistically update or refetch
    user.is_frozen = !user.is_frozen; // Optimistic update
    // Or store.dispatch('user/fetchAllUsers');
  } catch (err) {
    console.error('Failed to toggle freeze status:', err);
    // Display error
  } finally {
    actionLoading.value = null;
    currentAction.value = '';
  }
};

const toggleAdminStatus = async (user) => {
  actionLoading.value = user.id;
  currentAction.value = 'admin';
  try {
    await store.dispatch('user/updateUserAdmin', {
        userId: user.id,
        data: { is_staff: !user.is_staff }
    });
    user.is_staff = !user.is_staff; // Optimistic update
  } catch (err) {
    console.error('Failed to toggle admin status:', err);
  } finally {
    actionLoading.value = null;
    currentAction.value = '';
  }
};

const deleteUser = async (userId) => {
  if (!confirm(`确定要永久删除用户 ID: ${userId} 吗？此操作不可恢复。`)) return;
  actionLoading.value = userId;
  currentAction.value = 'delete';
  try {
    await store.dispatch('user/deleteUserAdmin', userId);
    // Refetch users after deletion
    store.dispatch('user/fetchAllUsers');
  } catch (err) {
    console.error('Failed to delete user:', err);
  } finally {
    actionLoading.value = null;
    currentAction.value = '';
  }
};
</script>

<style scoped>
.admin-user-manager {
  padding: 20px;
}
.admin-user-manager h2 {
  text-align: center;
  margin-bottom: 30px;
}
.user-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  border-radius: 8px;
  overflow: hidden; /* For border-radius on table */
}
.user-table th, .user-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}
.user-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
}
.user-table tbody tr:last-child td {
  border-bottom: none;
}
.user-table tbody tr:hover {
  background-color: #f1f3f5;
}
.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.85em;
  color: white;
  display: inline-block;
}
.status-badge.active { background-color: #28a745; } /* Green */
.status-badge.frozen { background-color: #ffc107; color: #212529;} /* Yellow */
.status-badge.inactive { background-color: #6c757d; } /* Gray */

.user-actions .action-btn {
  padding: 5px 8px;
  font-size: 0.85em;
  margin-right: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.user-actions .action-btn:last-child {
  margin-right: 0;
}
.freeze-btn { background-color: #17a2b8; color: white; } /* Teal */
.admin-toggle-btn { background-color: #fd7e14; color: white; } /* Orange */
.delete-btn { background-color: #dc3545; color: white; } /* Red */

.action-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>