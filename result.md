import { branchSchema } from "@/lib/validators";
import { z } from "zod";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useDebounce } from "@/hooks/use-debounce";

type BranchFormData = z.infer<typeof branchSchema>;

export default function BranchesPage() {
  const branches = useQuery(api.branches.getActive);
  const createBranch = useMutation(api.branches.create);
  const updateBranch = useMutation(api.branches.update);
  const deleteBranch = useMutation(api.branches.remove);

  const [isOpen, setIsOpen] = useState(false);
  const [editingBranch, setEditingBranch] = useState<any>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<any>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  const form = useForm<BranchFormData>({
    resolver: zodResolver(branchSchema),
    defaultValues: {
      name: "",
      code: "",
      address: "",
      phone: "",
    },
  });

  // Watch form values for real-time validation
  const watchedName = form.watch("name");
  const watchedCode = form.watch("code");
  const watchedPhone = form.watch("phone");
  const debouncedName = useDebounce(watchedName, 500);
  const debouncedCode = useDebounce(watchedCode, 500);
  const debouncedPhone = useDebounce(watchedPhone, 500);

  // Real-time availability check
  const availabilityCheck = useQuery(
    api.branches.checkAvailability,
    (debouncedName || debouncedCode) ? {
      name: debouncedName || undefined,
      code: debouncedCode || undefined,
      excludeId: editingBranch?._id,
    } : "skip"
  );

  if (!branches) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  const resetForm = () => {
    form.reset({
      name: "",
      code: "",
      address: "",
      phone: "",
    });
    setEditingBranch(null);
  };

  const handleOpen = (branch?: any) => {
    if (branch) {
      setEditingBranch(branch);
      form.reset({
        name: branch.name,
        code: branch.code,
        address: branch.address,
        phone: branch.phone,
      });
    } else {
      resetForm();
    }
    setIsOpen(true);
  };

  const handleSubmit = async (data: BranchFormData) => {
    setIsSubmitting(true);
    try {
      if (editingBranch) {
        await updateBranch({
          id: editingBranch._id,
          name: data.name,
          address: data.address,
          phone: data.phone,
          isActive: editingBranch.isActive,
        });
        toast.success("تم تحديث الفرع بنجاح");
      } else {
        await createBranch({
          ...data,
          isActive: true,
        });
        toast.success("تم إضافة الفرع بنجاح");
      }
      setIsOpen(false);
      resetForm();
    } catch (error: any) {
      toast.error(error.message || "حدث خطأ");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteConfirm) return;

    setIsDeleting(true);
    try {
      await deleteBranch({ id: deleteConfirm._id });
      toast.success("تم حذف الفرع بنجاح");
      setDeleteConfirm(null);
    } catch (error: any) {
      toast.error(error.message || "حدث خطأ");
    } finally {
      setIsDeleting(false);
    }
  };

  // Filter branches by search term
  const filteredBranches = branches.filter((branch: any) =>
    branch.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    branch.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    branch.phone.includes(searchTerm)
  );

  const activeBranches = branches?.length || 0;

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">   
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold flex items-center gap-2 text-gray-900 dark:text-white">
            <Building2 className="w-5 h-5 sm:w-8 sm:h-8 text-blue-600 dark:text-blue-400     

... [TRUNCATED - File has 25544 total characters]

[FILE]: app\dashboard\settings\roles\page.tsx
------------------------------------------------------------
"use client";

import { useQuery, useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";   
import { Label } from "@/components/ui/label";
import { AR_TEXT } from "@/lib/constants";
import { toast } from "sonner";
import { Edit, Trash2, Plus, Shield, Check, Users, AlertTriangle } from "lucide-react";      
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Skeleton } from "@/components/ui/skeleton";

// All available permissions with Arabic labels
const PERMISSION_LABELS: Record<string, string> = {
  view_dashboard: "عرض لوحة التحكم",
  manage_sales: "إدارة المبيعات",
  view_sales: "عرض المبيعات",
  manage_products: "إدارة المنتجات",
  view_products: "عرض المنتجات",
  manage_inventory: "إدارة المخزون",
  view_inventory: "عرض المخزون",
  manage_suppliers: "إدارة الموردين",
  view_suppliers: "عرض الموردين",
  view_reports: "عرض التقارير",
  manage_branches: "إدارة الفروع",
  manage_users: "إدارة المستخدمين",
  manage_settings: "إدارة الإعدادات",
  manage_roles: "إدارة الأدوار",
};

const ALL_PERMISSIONS = Object.keys(PERMISSION_LABELS);

export default function RolesPage() {
  const roles = useQuery(api.roles.getWithUserCount);
  const createRole = useMutation(api.roles.create);
  const updateRole = useMutation(api.roles.update);
  const deleteRole = useMutation(api.roles.remove);

  const [isOpen, setIsOpen] = useState(false);
  const [editingRole, setEditingRole] = useState<any>(null);

  const [formData, setFormData] = useState({
    name: "",
    displayName: "",
    permissions: [] as string[],
  });

  if (!roles) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  const handleOpen = (role?: any) => {
    if (role) {
      setEditingRole(role);
      setFormData({
        name: role.name,
        displayName: role.displayName,
        permissions: role.permissions || [],
      });
    } else {
      setEditingRole(null);
      setFormData({
        name: "",
        displayName: "",
        permissions: [],
      });
    }
    setIsOpen(true);
  };

  const togglePermission = (permission: string) => {
    setFormData(prev => ({
      ...prev,
      permissions: prev.permissions.includes(permission)
        ? prev.permissions.filter(p => p !== permission)
        : [...prev.permissions, permission],
    }));
  };

  const selectAllPermissions = () => {
    setFormData(prev => ({
      ...prev,
      permissions: ALL_PERMISSIONS,
    }));
  };

  const clearAllPermissions = () => {
    setFormData(prev => ({
      ...prev,
      permissions: [],
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name.trim() || !formData.displayName.trim()) {
      toast.error("الاسم والاسم المعروض مطلوبان");
      return;
    }

    if (formData.permissions.length === 0) {
      toast.error("يجب اختيار صلاحية واحدة على الأقل");
      return;
    }

    try {
      if (editingRole) {
        await updateRole({
          id: editingRole._id,
          displayName: formData.displayName,
          permissions: formData.permissions,
        });
        toast.success(AR_TEXT.updateSuccess);
      } else {
        await createRole({
          name: formData.name.toLowerCase().replace(/\s+/g, "_"),
          displayName: formData.displayName,
          permissions: formData.permissions,
        });
        toast.success(AR_TEXT.addSuccess);
      }
      setIsOpen(false);
    } catch (error: any) {
      toast.error(error.message || AR_TEXT.error);
    }
  };

  const handleDelete = async (id: any) => {
    if (confirm(AR_TEXT.deleteConfirm)) {
      try {
        await deleteRole({ id });
        toast.success(AR_TEXT.deleteSuccess);
      } catch (error: any) {
        toast.error(error.message || "فشل الحذف");
      }
    }
  };

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">   
        <h1 className="text-2xl sm:text-3xl font-bold flex items-center gap-2 text-gray-900 dark:text-white">
          <Shield className="w-5 h-5 sm:w-8 sm:h-8 text-purple-600 dark:text-purple-400" />  
          إدارة الأدوار والصلاحيات
        </h1>
        <Button onClick={() => handleOpen()} className="gap-2 w-full sm:w-auto bg-purple-600 hover:bg-purple-700 dark:bg-purple-600 dark:hover:bg-purple-700">
          <Plus className="w-4 h-4" />
          دور جديد
        </Button>
      </div>

      {/* Responsive Table Container */}
      <div className="bg-white dark:bg-gray

... [TRUNCATED - File has 14285 total characters]

[FILE]: app\dashboard\settings\users\page.tsx
------------------------------------------------------------
"use client";

import { useQuery, useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";   
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { AR_TEXT } from "@/lib/constants";
import { toast } from "sonner";
import { Edit, Trash2, Users, User } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Id } from "@/convex/_generated/dataModel";

export default function UsersPage() {
  const users = useQuery(api.users.getAll);
  const branches = useQuery(api.branches.getActive);
  const roles = useQuery(api.roles.getActive);
  const updateUser = useMutation(api.users.update);
  const deleteUser = useMutation(api.users.remove);

  const [isOpen, setIsOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<any>(null);

  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    roleId: "",
    branchId: "",
    isActive: true,
  });

  if (!users || !branches || !roles) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  const getRoleBadge = (roleId: Id<"roles"> | undefined) => {
    const role = roles?.find(r => r._id === roleId);
    if (!role) return <Badge variant="outline">غير محدد</Badge>;

    switch (role.name) {
      case "super_admin": return <Badge className="bg-purple-500 hover:bg-purple-600">{role.displayName}</Badge>;
      case "branch_manager": return <Badge className="bg-blue-500 hover:bg-blue-600">{role.displayName}</Badge>;
      case "cashier": return <Badge className="bg-green-500 hover:bg-green-600">{role.displayName}</Badge>;
      default: return <Badge variant="outline">{role.displayName}</Badge>;
    }
  };

  const handleOpen = (user?: any) => {
    if (user) {
      setEditingUser(user);
      setFormData({
        name: user.name,
        phone: user.phone || "",
        roleId: user.roleId || "",
        branchId: user.branchId || "",
        isActive: user.isActive,
      });
    } else {
      setEditingUser(null);
      setFormData({
        name: "",
        phone: "",
        roleId: "",
        branchId: "",
        isActive: true,
      });
    }
    setIsOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (!editingUser) {
        toast.error("المستخدمون يتم إنشاؤهم تلقائياً عبر Clerk.");
        return;
      }

      const payload: any = {
        id: editingUser._id,
        name: formData.name,
        isActive: formData.isActive,
      };

      if (formData.phone) payload.phone = formData.phone;
      if (formData.roleId) payload.roleId = formData.roleId as Id<"roles">;
      if (formData.branchId) payload.branchId = formData.branchId as Id<"branches">;

      await updateUser(payload);
      toast.success(AR_TEXT.updateSuccess);
      setIsOpen(false);
    } catch (error: any) {
      toast.error(error.message || AR_TEXT.error);
    }
  };

  const handleDelete = async (id: any) => {
    if (confirm(AR_TEXT.deleteConfirm)) {
      try {
        await deleteUser({ id });
        toast.success(AR_TEXT.deleteSuccess);
      } catch (e) {
        toast.error("فشل الحذف");
      }
    }
  };

  const selectedRole = roles?.find(r => r._id === formData.roleId);
  const showBranchSelect = selectedRole?.name !== "super_admin";

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">   
        <h1 className="text-2xl sm:text-3xl font-bold flex items-center gap-2 text-gray-900 dark:text-white">
          <Users className="w-5 h-5 sm:w-8 sm:h-8 text-green-600 dark:text-green-400" />     
          {AR_TEXT.userManagement}
        </h1>
        <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400">
          المستخدمون يتم إنشاؤهم تلقائياً عند تسجيل الدخول عبر Clerk
        </p>
      </div>

      {/* Responsive Table Container */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden border border-gray-200 dark:border-gray-700">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="text-right min-w-[120px] text-gray-900 dark:text-gray-100">{AR_TEXT.userName}</TableHead>
                <TableHead className="text-right min-w-[150px] hidden md:table-cell text-gray-900 dark

... [TRUNCATED - File has 13942 total characters]

[FILE]: app\dashboard\skills\page.tsx
------------------------------------------------------------
"use client";

import * as React from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Sparkles, Plus, Edit, Trash2, GripVertical } from "lucide-react";
import { cn } from "@/lib/utils";

const sampleSkills = [
  { id: "1", name: "Python", category: "Programming", level: 95 },
  { id: "2", name: "SQL", category: "Database", level: 90 },
  { id: "3", name: "Azure Data Factory", category: "Cloud", level: 85 },
  { id: "4", name: "Apache Spark", category: "Big Data", level: 80 },
  { id: "5", name: "Power BI", category: "Visualization", level: 85 },
  { id: "6", name: "Databricks", category: "Big Data", level: 75 },
  { id: "7", name: "PostgreSQL", category: "Database", level: 88 },
  { id: "8", name: "Apache Airflow", category: "Orchestration", level: 82 },
];

const categories = ["All", "Programming", "Database", "Cloud", "Big Data", "Visualization", "Orchestration"];

export default function SkillsPage() {
  const [selectedCategory, setSelectedCategory] = React.useState("All");

  const filteredSkills = selectedCategory === "All"
    ? sampleSkills
    : sampleSkills.filter(skill => skill.category === selectedCategory);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Skills</h1>
          <p className="text-muted-foreground">Manage your technical skills and expertise</p>
        </div>
        <Button className="gap-2">
          <Plus className="w-4 h-4" />
          Add Skill
        </Button>
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2">
        {categories.map((category) => (
          <Button
            key={category}
            variant={selectedCategory === category ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedCategory(category)}
            className="rounded-full"
          >
            {category}
          </Button>
        ))}
      </div>

      {/* Skills Grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {filteredSkills.map((skill) => (
          <Card key={skill.id} className="group relative overflow-hidden border-border/50 hover:shadow-md transition-all duration-300">
            <CardContent className="p-4">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-yellow-500/20 to-yellow-500/5 flex items-center justify-center shrink-0">
                  <Sparkles className="w-5 h-5 text-yellow-500" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium truncate">{skill.name}</h3>
                  <p className="text-xs text-muted-foreground">{skill.category}</p>
                </div>
                <GripVertical className="w-4 h-4 text-muted-foreground/50 cursor-grab" />    
              </div>

              {/* Skill Level Bar */}
              <div className="mb-3">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-muted-foreground">Proficiency</span>
                  <span className="font-medium">{skill.level}%</span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-primary to-primary/80 rounded-full transition-all duration-500"
                    style={{ width: `${skill.level}%` }}
                  />
                </div>
              </div>

              <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <Button variant="outline" size="sm" className="flex-1 gap-1.5 h-8">
                  <Edit className="w-3 h-3" />
                  Edit
                </Button>
                <Button variant="outline" size="icon" className="shrink-0 h-8 w-8 hover:text-destructive hover:border-destructive">
                  <Trash2 className="w-3 h-3" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}

        {/* Add Skill Card */}
        <Card className="border-2 border-dashed border-border/60 hover:border-primary/50 transition-colors cursor-pointer group min-h-[180px]">
          <CardContent className="h-full flex flex-col items-center justify-center p-4 text-center">
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-3 group-hover:bg-primary/20 transition-colors">
              <Plus className="w-6 h-6 text-primary" />
            </div>
            <h3 className="font-semibold text-sm mb-0.5">Add New Skill</h3>
            <p className="text-xs text-muted-foreground">Add your expertise</p>
          </CardContent>
        </Card>


... [TRUNCATED - File has 5025 total characters]

[FILE]: app\dashboard\suppliers\page.tsx
------------------------------------------------------------
"use client";

import { useState } from "react";
import { useQuery, useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { AR_TEXT } from "@/lib/constants";
import { Plus, Edit, Trash2, Search } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { toast } from "sonner";
import { Skeleton } from "@/components/ui/skeleton";
import { SupplierForm } from "@/components/suppliers/supplier-form";
import { Input } from "@/components/ui/input";
import { Truck } from "lucide-react";

export default function SuppliersPage() {
  const suppliers = useQuery(api.suppliers.getAll);
  const deleteSupplier = useMutation(api.suppliers.remove);
  const updateSupplier = useMutation(api.suppliers.update);

  const [editingSupplier, setEditingSupplier] = useState<any>(null);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredSuppliers = suppliers?.filter(s =>
    s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.phone.includes(searchTerm) ||
    (s.email && s.email.toLowerCase().includes(searchTerm.toLowerCase()))
  ) || [];

  const handleDelete = async (id: any) => {
    if (confirm(AR_TEXT.deleteConfirm)) {
      await deleteSupplier({ id });
      toast.success(AR_TEXT.deleteSuccess);
    }
  };

  const handleEdit = (supplier: any) => {
    setEditingSupplier(supplier);
    setIsEditOpen(true);
  };

  const handleUpdate = async (formData: any) => {
    if (!editingSupplier) return;

    try {
      await updateSupplier({
        id: editingSupplier._id,
        name: formData.name,
        phone: formData.phone,
        email: formData.email || undefined,
        address: formData.address,
        taxNumber: formData.taxNumber || undefined,
        notes: formData.notes || undefined,
        isActive: true,
      });
      toast.success("تم التعديل بنجاح");
      setIsEditOpen(false);
      setEditingSupplier(null);
    } catch (error: any) {
      toast.error(error.message || "حصل خطأ");
    }
  };

  if (!suppliers) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-32" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Header - Responsive */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">   
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">      
            {AR_TEXT.suppliers}
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {filteredSuppliers.length} مورد
          </p>
        </div>
        <AddSupplierDialog />
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
        <Input
          placeholder="بحث عن مورد..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pr-9 bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white"
        />
      </div>

      {/* Responsive Table Container */}
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow border border-gray-200 dark:border-gray-800 overflow-hidden">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow className="border-b border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                <TableHead className="text-gray-700 dark:text-gray-300 min-w-[120px]">{AR_TEXT.supplierName}</TableHead>
                <TableHead className="text-gray-700 dark:text-gray-300 min-w-[120px]">{AR_TEXT.phone}</TableHead>
                <TableHead className="text-gray-700 dark:text-gray-300 min-w-[150px] hidden md:table-cell">{AR_TEXT.address}</TableHead>
                <TableHead className="text-gray-700 dark:text-gray-300 min-w-[120px] hidden lg:table-cell">{AR_TEXT.taxNumber}</TableHead>
                <TableHead className="text-gray-700 dark:text-gray-300 min-w-[100px]">{AR_TEXT.actions}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredSuppliers.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-12 text-gray-500 dark:text-gray-400">
                    <Truck className="w-12 h-12 mx-auto text-gray-400 dark:text-gray-600 mb-3" />
                    <p>لا توجد موردين</p>
                  </TableCell>
                </TableRow>
              ) : (
                filteredSuppliers.map((s) => (
                  <TableRow key={s._id} c

... [TRUNCATED - File has 8409 total characters]

[FILE]: app\seed\page.tsx
------------------------------------------------------------
"use client";

import { useQuery, useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { useUser } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, Loader2, Package, Building2, Users, ShoppingBag } from "lucide-react"; 

export default function SeedPage() {
  const { user, isLoaded } = useUser();
  const router = useRouter();
  const [isSeeding, setIsSeeding] = useState(false);
  const [seededItems, setSeededItems] = useState<string[]>([]);

  const createBranch = useMutation(api.branches.create);
  const createSupplier = useMutation(api.suppliers.create);
  const createProduct = useMutation(api.products.create);
  const createVariant = useMutation(api.productVariants.create);
  const upsertInventory = useMutation(api.inventory.upsert);
  const seedRoles = useMutation(api.seedRoles.seedDefaultRoles);

  // Check if user has admin role
  const currentUser = useQuery(
    api.users.getByClerkId,
    user?.id ? { clerkId: user.id } : "skip"
  );

  // Check existing data
  const branches = useQuery(api.branches.getAll);
  const suppliers = useQuery(api.suppliers.getAll);
  const products = useQuery(api.products.getAll);
  const roles = useQuery(api.roles.getAll);

  const hasAccess = currentUser && (currentUser as any).isActive;
  const hasBranches = branches && branches.length > 0;
  const hasProducts = products && products.length > 0;
  const hasRoles = roles && roles.length > 0;

  const handleSeedRoles = async () => {
    setIsSeeding(true);
    try {
      const result = await seedRoles();
      toast.success(result.message);
      setSeededItems(prev => [...prev, "roles"]);
    } catch (error: any) {
      toast.error(error.message || "حدث خطأ");
    } finally {
      setIsSeeding(false);
    }
  };

  const handleSeedData = async () => {
    setIsSeeding(true);
    try {
      // 1. Create Branch
      let branchId;
      if (!hasBranches) {
        branchId = await createBranch({
          name: "الفرع الرئيسي",
          code: "MAIN-01",
          address: "شارع التحرير، وسط البلد، القاهرة",
          phone: "01012345678",
          isActive: true,
        });
        toast.success("تم إنشاء الفرع");
      } else {
        branchId = branches![0]._id;
      }

      // 2. Create Supplier
      let supplierId;
      if (!suppliers || suppliers.length === 0) {
        supplierId = await createSupplier({
          name: "مورد الملابس الرئيسي",
          address: "وسط البلد، القاهرة",
          phone: "01123456789",
          isActive: true,
        });
        toast.success("تم إنشاء المورد");
      } else {
        supplierId = suppliers[0]._id;
      }

      // 3. Create Products with Variants and Inventory
      if (!hasProducts) {
        const sampleProducts = [
          {
            name: "تيشيرت قطن",
            description: "تيشيرت قطن مصري عالي الجودة",
            category: "ملابس رجالي",
            basePrice: 250,
            barcode: "TSH-001",
          },
          {
            name: "بنطلون جينز",
            description: "بنطلون جينز قصة مستقيمة",
            category: "ملابس رجالي",
            basePrice: 450,
            barcode: "JNS-001",
          },
          {
            name: "فستان صيفي",
            description: "فستان مشجر خفيف",
            category: "ملابس حريمي",
            basePrice: 600,
            barcode: "DRS-001",
          },
        ];

        for (const p of sampleProducts) {
          const productId = await createProduct({
            ...p,
            images: [],
            supplierId: supplierId,
            isActive: true,
          });

          // Add Variants
          const sizes = ["M", "L", "XL"];
          const colors = [
            { name: "أبيض", hex: "#FFFFFF" },
            { name: "أسود", hex: "#000000" },
          ];

          for (const size of sizes) {
            for (const color of colors) {
              const variantId = await createVariant({
                productId,
                sku: `${p.barcode}-${size}-${color.name}`,
                size,
                color: color.name,
                colorHex: color.hex,
                barcode: `${p.barcode}-${size}-${color.name}`,
                additionalPrice: 0,
                isActive: true,
              });

              // Add Inventory
              await upsertInventory({
                productVariantId: variantId,
                branchId,
                quantity: 50,
                minStockLevel: 5,
              });
            }
          }
        }
        toast.success("تم إنشاء المنتجات والمخزون");
      }

      toast.success("تم إضافة البيانات التجريبية بنجاح");
      setSeededItems(prev => [...prev, "data"]);
    } catch (

... [TRUNCATED - File has 10352 total characters]

[FILE]: app\sign-in\[[...sign-in]]\page.tsx
------------------------------------------------------------
"use client";

import { SignIn } from "@clerk/nextjs";

export default function SignInPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <SignIn />
    </div>
  );
}


[FILE]: app\sign-up\[[...sign-up]]\page.tsx
------------------------------------------------------------
"use client";

import { SignUp } from "@clerk/nextjs";

export default function SignUpPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <SignUp />
    </div>
  );
}


================================================================================
ALL TSX/TS/JSX/JS FILES
================================================================================
  middleware.ts
  next-env.d.ts
  next.config.ts
  app\layout.tsx
  app\page.tsx
  app\dashboard\layout.tsx
  app\dashboard\page.tsx
  app\dashboard\experience\page.tsx
  app\dashboard\hero\page.tsx
  app\dashboard\inventory\page.tsx
  app\dashboard\messages\page.tsx
  app\dashboard\products\page.tsx
  app\dashboard\projects\page.tsx
  app\dashboard\reports\page.tsx
  app\dashboard\sales\page.tsx
  app\dashboard\sales\new\page.tsx
  app\dashboard\settings\page.tsx
  app\dashboard\settings\branches\page.tsx
  app\dashboard\settings\roles\page.tsx
  app\dashboard\settings\users\page.tsx
  app\dashboard\skills\page.tsx
  app\dashboard\suppliers\page.tsx
  app\seed\page.tsx
  app\sign-in\[[...sign-in]]\page.tsx
  app\sign-up\[[...sign-up]]\page.tsx
  components\ConvexClientProvider.tsx
  components\error-boundary.tsx
  components\ThemeProvider.tsx
  components\ThemeToggle.tsx
  components\UserSync.tsx
  components\dashboard\Header.tsx
  components\dashboard\MobileSidebar.tsx
  components\dashboard\Sidebar.tsx
  components\products\add-product-dialog.tsx
  components\products\edit-product-dialog.tsx
  components\products\product-form.tsx
  components\suppliers\supplier-form.tsx
  components\ui\avatar.tsx
  components\ui\badge.tsx
  components\ui\button.tsx
  components\ui\calendar.tsx
  components\ui\card.tsx
  components\ui\dialog.tsx
  components\ui\dropdown-menu.tsx
  components\ui\input.tsx
  components\ui\label.tsx
  components\ui\phone-input.tsx
  components\ui\popover.tsx
  components\ui\scroll-area.tsx
  components\ui\searchable-select.tsx
  ... and 35 more files

================================================================================
ANALYSIS COMPLETE
================================================================================