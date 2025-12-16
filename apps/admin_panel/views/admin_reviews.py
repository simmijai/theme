from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from apps.store.models import Review

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def admin_review_list(request):
    reviews = Review.objects.select_related('product', 'user', 'order').order_by('-created_at')
    
    # Filter by approval status
    status = request.GET.get('status')
    if status == 'approved':
        reviews = reviews.filter(is_approved=True)
    elif status == 'pending':
        reviews = reviews.filter(is_approved=False)
    
    # Filter by rating
    rating = request.GET.get('rating')
    if rating:
        reviews = reviews.filter(rating=rating)
    
    # Search by product name or user
    search = request.GET.get('search')
    if search:
        reviews = reviews.filter(
            Q(product__name__icontains=search) | 
            Q(user__first_name__icontains=search) |
            Q(user__email__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(reviews, 10)
    page = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'admin_theme/reviews/review_list.html', {
        'reviews': page,
        'status': status,
        'rating': rating,
        'search': search
    })


def admin_review_edit(request, review_id):
    try:
        review = get_object_or_404(Review, id=review_id)
        if request.method == 'POST':
            try:
                rating = request.POST.get('rating')
                comment = request.POST.get('comment', '').strip()
                
                # Validate and sanitize rating
                try:
                    rating = int(rating)
                    if rating < 1 or rating > 5:
                        raise ValueError
                except (ValueError, TypeError):
                    rating = review.rating  # Keep original if invalid
                    messages.warning(request, 'Invalid rating provided. Keeping original rating.')
                
                # Sanitize comment
                import re
                comment = re.sub(r'\s+', ' ', comment)
                if len(comment) > 1000:  # Limit comment length
                    comment = comment[:1000]
                    messages.warning(request, 'Comment was truncated to 1000 characters.')
                
                review.rating = rating
                review.comment = comment
                review.is_approved = 'is_approved' in request.POST

                if request.FILES.get('image'):
                    review.image = request.FILES.get('image')

                review.save()
                messages.success(request, 'Review updated successfully!')
                return redirect('admin_review_list')
            except Exception as e:
                messages.error(request, 'Error updating review. Please try again.')

        return render(request, 'admin_theme/reviews/review_edit.html', {'review': review})
    except Exception as e:
        messages.error(request, 'Error loading review. Please try again.')
        return redirect('admin_review_list')

# @user_passes_test(is_admin)
def admin_review_delete(request, review_id):
    try:
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        messages.success(request, 'Review deleted successfully!')
    except Exception as e:
        messages.error(request, 'Error deleting review. Please try again.')
    return redirect('admin_review_list')

def admin_review_toggle(request, review_id):
    try:
        review = get_object_or_404(Review, id=review_id)
        review.is_approved = not review.is_approved
        review.save()
        status = 'approved' if review.is_approved else 'unapproved'
        messages.success(request, f'Review {status} successfully!')
    except Exception as e:
        messages.error(request, 'Error updating review status. Please try again.')
    return redirect('admin_review_list')
