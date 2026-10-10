from django.core.management.base import BaseCommand
from django.db import transaction
from mocktests.models import Mock_Test, Question


class Command(BaseCommand):
    help = 'Seeds the database with the Math for AI & DS ISA-1 Mock Test (Sem 3)'

    def handle(self, *args, **kwargs):
        self.create_math_ai_test()

    def _bulk_create_questions(self, test, questions_data):
        objs = [
            Question(
                test=test,
                question_desc=q['desc'],
                option_a=q['a'], option_b=q['b'],
                option_c=q['c'], option_d=q['d'],
                correct_answer=q['ans'],
                marks=q['marks'],
                explanation=q['exp'],
            )
            for q in questions_data
        ]
        Question.objects.bulk_create(objs)
        total = sum(q['marks'] for q in questions_data)
        one = sum(1 for q in questions_data if q['marks'] == 1)
        two = sum(1 for q in questions_data if q['marks'] == 2)
        self.stdout.write(self.style.SUCCESS(
            f'  -> {len(questions_data)} questions | 1-markers: {one} | '
            f'2-markers: {two} | Total marks: {total}'
        ))

    @transaction.atomic
    def create_math_ai_test(self):
        test, created = Mock_Test.objects.get_or_create(
            title="Math for AI & DS ISA-1 Mock Test",
            defaults={
                'description': (
                    "Linear Algebra for AI & DS. Fundamental Subspaces, LU/LDU, "
                    "QR, SVD, Projections, Eigenvalues, PCA, Positive Definite. "
                    "30 questions, 40 marks, 65 minutes."
                ),
                'course_name': "Mathematics for AI & DS",
                'semester': 3,
                'total_qns': 30,
                'duration': 65,
            }
        )
        if not created:
            Question.objects.filter(test=test).delete()
            test.total_qns = 30
            test.duration = 65
            test.save()

        self.stdout.write(self.style.SUCCESS(f'Creating Questions for "{test.title}"...'))

        questions_data = [
            # ==================================================
            # 2-MARKERS (10 × 2 = 20 marks)
            # ==================================================
            {
                'desc': (
                    'For the matrix A = [[1, 2, 3], [1, 1, 1], [2, 4, 6]], '
                    'what is the basis of the Column Space C(A)?'
                ),
                'a': '{(1,1,2), (2,1,4)} — the pivot columns of A',
                'b': '{(1,2,3), (1,1,1), (2,4,6)}',
                'c': '{(1,0,0), (0,1,0), (0,0,1)}',
                'd': '{(3,1,6)} only',
                'ans': 'A', 'marks': 2,
                'exp': 'After row reduction, the pivots are in columns 1 and 2 of A. The basis of C(A) is {(1,1,2), (2,1,4)}. The third column is a multiple of the first.'
            },
            {
                'desc': (
                    'For the matrix A = [[1,2,3],[1,1,1],[2,4,6]], the row space Row(A) '
                    'is spanned by which rows?'
                ),
                'a': 'Row 1 and Row 2 of A',
                'b': 'Row 1, Row 2, and Row 3 of A',
                'c': 'Row 3 only',
                'd': 'All three rows are independent',
                'ans': 'A', 'marks': 2,
                'exp': 'Row 3 = 2 × Row 1, so it is not independent. The row space is spanned by Rows 1 and 2.'
            },
            {
                'desc': (
                    'Find the projection of b = (1, 2, 7) onto the column space of A '
                    'spanned by (1, 1, 7, 2) and (1, -1, 4). What is the projection vector p?'
                ),
                'a': 'Approximately (2, 0, 11, 2)',
                'b': '(1, 2, 7) exactly',
                'c': '(0, 0, 0)',
                'd': '(1, 1, 7)',
                'ans': 'A', 'marks': 2,
                'exp': 'Using least squares: p = A(AᵀA)⁻¹Aᵀb. Solving gives p ≈ (2, 0, 11, 2).'
            },
            {
                'desc': (
                    'A = [[1, 1, 0]]. Compute A Aᵀ. What are its eigenvalues?'
                ),
                'a': 'λ₁ = 3, λ₂ = 1', 'b': 'λ₁ = 2, λ₂ = 0',
                'c': 'λ₁ = 1, λ₂ = 1', 'd': 'λ₁ = 4, λ₂ = 2',
                'ans': 'A', 'marks': 2,
                'exp': 'A = [[1,1,0]], so A Aᵀ = [[2, 1],[1, 2]]. det(A Aᵀ − λI) = (2−λ)² − 1 = 0 → λ = 3 or 1. Singular values: σ₁=√3, σ₂=1.'
            },
            {
                'desc': (
                    'For what value of k is the system x + y = 2, 2x + 2y = k consistent?'
                ),
                'a': 'k = 4', 'b': 'k = 2', 'c': 'k = 0', 'd': 'k = any value',
                'ans': 'A', 'marks': 2,
                'exp': 'For consistency, the second equation must be 2× the first: k = 4. Otherwise the system is inconsistent (parallel lines).'
            },
            {
                'desc': (
                    'For what value of h are the vectors v₁ = (1,2,3), v₂ = (2,4,h), '
                    'v₃ = (1,2,3) linearly independent?'
                ),
                'a': 'Never — v₁ and v₃ are identical',
                'b': 'h ≠ 6', 'c': 'h = 6', 'd': 'h = 0',
                'ans': 'A', 'marks': 2,
                'exp': 'v₁ and v₃ are the same vector, so the set is always linearly dependent regardless of h.'
            },
            {
                'desc': (
                    'Let T: ℝ² → ℝ² be T(x, y) = (x + y, x − y + 2). '
                    'Which statement is correct?'
                ),
                'a': 'T is not linear because T(0,0) = (0, 2) ≠ (0,0)',
                'b': 'T is linear because both components are linear',
                'c': 'T is linear but not invertible',
                'd': 'T is linear only when x + y > 0',
                'ans': 'A', 'marks': 2,
                'exp': 'A linear transformation must map the origin to the origin. T(0,0) = (0, 2) ≠ (0,0), so T is not linear.'
            },
            {
                'desc': (
                    'A = [[4, 1], [2, 3]]. What are its eigenvalues?'
                ),
                'a': 'λ₁ = 5, λ₂ = 2', 'b': 'λ₁ = 4, λ₂ = 3',
                'c': 'λ₁ = 6, λ₂ = 1', 'd': 'λ₁ = 3, λ₂ = 4',
                'ans': 'A', 'marks': 2,
                'exp': 'det(A − λI) = (4−λ)(3−λ) − 2 = λ² − 7λ + 10 = 0 → λ = 5 or 2.'
            },
            {
                'desc': (
                    'A 3×3 matrix A has eigenvalues 2, 3, λ. If Trace(A) = 10, what is det(A)?'
                ),
                'a': '30', 'b': '10', 'c': '6', 'd': '60',
                'ans': 'A', 'marks': 2,
                'exp': 'Trace = sum of eigenvalues → 2 + 3 + λ = 10 → λ = 5. det(A) = product = 2 × 3 × 5 = 30.'
            },
            {
                'desc': (
                    'For what range of b is the matrix [[1, b], [b, 9]] positive definite?'
                ),
                'a': '−3 < b < 3', 'b': 'b > 0',
                'c': 'b < 9', 'd': 'b = 0 only',
                'ans': 'A', 'marks': 2,
                'exp': 'Leading principal minors: det(1) = 1 > 0 ✓; det = 9 − b² > 0 → b² < 9 → −3 < b < 3.'
            },

            # ==================================================
            # 1-MARKERS (20 × 1 = 20 marks)
            # ==================================================
            {
                'desc': (
                    'Let T: ℝ² → ℝ² be T(x, y) = (2x + y, x − 3y). '
                    'What is the matrix of T with respect to the standard basis?'
                ),
                'a': '[[2, 1], [1, -3]]', 'b': '[[2, 1], [3, -1]]',
                'c': '[[1, 2], [-3, 1]]', 'd': '[[2, -3], [1, 1]]',
                'ans': 'A', 'marks': 1,
                'exp': 'Columns are images of basis vectors: T(1,0) = (2,1), T(0,1) = (1,−3). Matrix = [[2,1],[1,−3]].'
            },
            {
                'desc': (
                    'A = [a_ij] is a 3×4 matrix with a_ij = (−1)^j. What is rank(A)?'
                ),
                'a': '1', 'b': '3', 'c': '4', 'd': '0',
                'ans': 'A', 'marks': 1,
                'exp': 'Each column has constant entries (−1 or 1). All columns are multiples of each other. Only 1 linearly independent row → rank = 1.'
            },
            {
                'desc': (
                    'Let W = {(x, y, z) ∈ ℝ³ : x + y + z = 0}. What is the dimension of W?'
                ),
                'a': '2', 'b': '3', 'c': '1', 'd': '0',
                'ans': 'A', 'marks': 1,
                'exp': 'One constraint reduces ℝ³ to a plane through the origin. Dimension = 3 − 1 = 2. Basis: {(1, −1, 0), (1, 0, −1)}.'
            },
            {
                'desc': (
                    'Which transformation T: ℝ² → ℝ² is linear?'
                ),
                'a': 'T(x, y) = (2x + y, x − y)',
                'b': 'T(x, y) = (x², y)',
                'c': 'T(x, y) = (x + 1, y)',
                'd': 'T(x, y) = (xy, y)',
                'ans': 'A', 'marks': 1,
                'exp': 'Only A has both components as linear combinations of x and y. B has x², C has a constant, D has xy.'
            },
            {
                'desc': (
                    'If the rank of a 3×3 matrix A is 2, then the set of all vectors Ax forms:'
                ),
                'a': 'A plane through the origin in ℝ³',
                'b': 'A line through the origin',
                'c': 'All of ℝ³',
                'd': 'The origin only',
                'ans': 'A', 'marks': 1,
                'exp': 'Rank = dimension of column space = 2 → image is a 2D subspace (plane) of ℝ³.'
            },
            {
                'desc': (
                    'Which property of a projection matrix P is FALSE?'
                ),
                'a': 'P is always invertible',
                'b': 'P² = P',
                'c': 'P = Pᵀ',
                'd': 'P has eigenvalues 0 or 1',
                'ans': 'A', 'marks': 1,
                'exp': 'A projection matrix is not invertible (unless it is the identity). P² = P, P = Pᵀ, and eigenvalues are 0 or 1.'
            },
            {
                'desc': (
                    'What is the shape/property of any covariance matrix?'
                ),
                'a': 'Always symmetric', 'b': 'Always diagonal',
                'c': 'Always skew-symmetric', 'd': 'Always upper triangular',
                'ans': 'A', 'marks': 1,
                'exp': 'A covariance matrix is always symmetric: Cov(X, Y) = Cov(Y, X).'
            },
            {
                'desc': (
                    'PCA uses an orthogonal transformation. What does "orthogonal" ensure about the principal components?'
                ),
                'a': 'The principal components are uncorrelated and mutually perpendicular',
                'b': 'The principal components are all equal',
                'c': 'The principal components are only positive numbers',
                'd': 'The principal components have unit variance',
                'ans': 'A', 'marks': 1,
                'exp': 'Orthogonal transformation means the resulting principal components are uncorrelated (mutually perpendicular in feature space), so they capture independent directions of variance.'
            },
            {
                'desc': (
                    'If Q is an orthogonal matrix, what is QᵀQ?'
                ),
                'a': 'I (the identity matrix)', 'b': 'Q',
                'c': 'Q²', 'd': 'A zero matrix',
                'ans': 'A', 'marks': 1,
                'exp': 'For an orthogonal matrix, columns are orthonormal: QᵀQ = QQᵀ = I.'
            },
            {
                'desc': (
                    'The sum of the eigenvalues of a square matrix A equals:'
                ),
                'a': 'The trace of A', 'b': 'The determinant of A',
                'c': 'The rank of A', 'd': 'Zero always',
                'ans': 'A', 'marks': 1,
                'exp': 'Sum of eigenvalues = trace of A. Product of eigenvalues = determinant of A.'
            },
            {
                'desc': (
                    'In least squares, the residual e = b − p is always:'
                ),
                'a': 'Orthogonal to the column space of A',
                'b': 'Parallel to the column space of A',
                'c': 'Zero', 'd': 'Equal to b',
                'ans': 'A', 'marks': 1,
                'exp': 'The residual b − p is orthogonal to the column space of A. That is what makes p the closest point in C(A) to b.'
            },
            {
                'desc': (
                    'PCA reduces dimensionality by keeping components with:'
                ),
                'a': 'The largest eigenvalues of the covariance matrix',
                'b': 'The smallest eigenvalues',
                'c': 'The largest negative eigenvalues',
                'd': 'All eigenvalues equally',
                'ans': 'A', 'marks': 1,
                'exp': 'PCA keeps directions of maximum variance, which correspond to the largest eigenvalues of the covariance matrix.'
            },
            {
                'desc': (
                    'If a matrix A is diagonalizable as A = SΛS⁻¹, then A⁶⁵ equals:'
                ),
                'a': 'SΛ⁶⁵S⁻¹', 'b': 'S⁶⁵ΛS⁻¹',
                'c': 'SΛS⁻¹ × 65', 'd': '65Λ',
                'ans': 'A', 'marks': 1,
                'exp': 'Diagonalization property: Aⁿ = SΛⁿS⁻¹. So A⁶⁵ = SΛ⁶⁵S⁻¹.'
            },
            {
                'desc': (
                    'A = [[3, 4, 2], [0, 1, 2], [0, 0, 2]] has eigenvalues 3, 1, 2. '
                    'What are the eigenvalues of A + I?'
                ),
                'a': '4, 2, 3', 'b': '3, 1, 2',
                'c': '4, 4, 3', 'd': '0, 0, 1',
                'ans': 'A', 'marks': 1,
                'exp': 'If λ is an eigenvalue of A, then λ + c is an eigenvalue of A + cI. So 3+1=4, 1+1=2, 2+1=3.'
            },
            {
                'desc': (
                    'For a matrix A_{n×n} with N(A) = {0} (nullspace is trivial), '
                    'which of the following is FALSE?'
                ),
                'a': 'A is singular', 'b': 'rank(A) = n',
                'c': 'A is invertible', 'd': 'det(A) ≠ 0',
                'ans': 'A', 'marks': 1,
                'exp': 'If the nullspace is trivial, A is nonsingular (invertible), rank n, det ≠ 0. Calling it singular is FALSE.'
            },
            {
                'desc': (
                    'The dimension of the subspace of all 2×2 symmetric matrices is:'
                ),
                'a': '3', 'b': '4', 'c': '2', 'd': '1',
                'ans': 'A', 'marks': 1,
                'exp': 'A 2×2 symmetric matrix has 3 free entries: [[a, b], [b, c]]. Basis dimension = 3.'
            },
            {
                'desc': (
                    'A = [[1, 4, -2], [1, 7, -6], [0, 3, q]]. Which value of q makes '
                    'the system singular?'
                ),
                'a': 'q = -4', 'b': 'q = 4', 'c': 'q = 0', 'd': 'q = 2',
                'ans': 'A', 'marks': 1,
                'exp': 'After row operations, q = −4 removes the last pivot, making the matrix singular (rank < 3).'
            },
            {
                'desc': (
                    'A 3×3 matrix A has eigenvalues 2, −1, 3, 0 — wait, that is 4 values. '
                    'For a 4×4 matrix with eigenvalues 2, −1, 3, 0, which is FALSE?'
                ),
                'a': 'A is invertible', 'b': 'det(A) = 0',
                'c': 'trace(A) = 4', 'd': 'A has a zero eigenvalue',
                'ans': 'A', 'marks': 1,
                'exp': 'One eigenvalue is 0, so det(A) = 0, meaning A is singular (not invertible). Saying A is invertible is FALSE.'
            },
            {
                'desc': (
                    'Which of the following matrices is diagonalizable?'
                ),
                'a': 'A matrix with n distinct eigenvalues',
                'b': 'Any singular matrix',
                'c': 'Any symmetric matrix with repeated eigenvalues',
                'd': 'Any matrix with only one eigenvalue',
                'ans': 'A', 'marks': 1,
                'exp': 'A matrix with n distinct eigenvalues always has n linearly independent eigenvectors, so it is diagonalizable.'
            },
            {
                'desc': (
                    'Let V = span{(1, 1, 0)} in ℝ³. What is the orthogonal complement V⊥?'
                ),
                'a': 'All (x, y, z) with x + y = 0',
                'b': 'All (x, y, z) with x = y',
                'c': 'All (x, y, z) with z = 0',
                'd': 'Only the zero vector',
                'ans': 'A', 'marks': 1,
                'exp': 'Orthogonal complement of (1,1,0) is the set of vectors (x,y,z) satisfying x·1 + y·1 + z·0 = 0, i.e., x + y = 0. Dimension = 2.'
            },
        ]

        self._bulk_create_questions(test, questions_data)