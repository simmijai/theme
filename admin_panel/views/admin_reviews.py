from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from store.models import Review

def is_admin(user):
    return user.is_staff or user.is_superuser

# @user_passes_test(is_admin)
def admin_review_list(request):
    reviews = Review.objects.select_related('product', 'user', 'order').order_by('-created_at')
    return render(request, 'admin/reviews/review_list.html', {'reviews': reviews})

# @user_passes_test(is_admin)
def admin_review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.rating = request.POST.get('rating')
        review.comment = request.POST.get('comment')
        if request.FILES.get('image'):
            review.image = request.FILES.get('image')
        review.save()
        return redirect('admin_review_list')
    return render(request, 'admin/reviews/review_edit.html', {'review': review})

# @user_passes_test(is_admin)
def admin_review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('admin_review_list')
